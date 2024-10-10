from dataclasses import asdict
import MySQLdb
from datetime import timedelta, datetime
import calendar

from exsited.exsited.order.dto.usage_dto import UsageCreateDTO, UsageDataDTO
from service.exsited_service import ExsitedService
from service.order_service import OrderService


def connect_to_db():
    return MySQLdb.connect(
        host="",
        user="",
        passwd="",
        db=""
    )


def calculate_charging_period(start_date):
    next_month = start_date.month + 1 if start_date.month < 12 else 1
    next_year = start_date.year if start_date.month < 12 else start_date.year + 1

    last_day_of_next_month = calendar.monthrange(next_year, next_month)[1]
    end_day = min(start_date.day, last_day_of_next_month)

    end_of_period = datetime(next_year, next_month, end_day) - timedelta(days=1)

    charging_period = f"{start_date.strftime('%Y-%m-%d')}-{end_of_period.strftime('%Y-%m-%d')}"
    return charging_period


def create_usage_dto(charge_item_uuid: str, quantity: str, start_time: str, end_time: str, charging_period: str):
    usage_data = UsageCreateDTO(
        usage=UsageDataDTO(chargeItemUuid=charge_item_uuid,
                           quantity=quantity,
                           startTime=start_time,
                           endTime=end_time,
                           type="INCREMENTAL",
                           chargingPeriod=charging_period
                           )
    )

    return usage_data


def fetch_call_usage():
    db = connect_to_db()
    cursor = db.cursor()

    try:
        cursor.execute(
            "SELECT CallID, CallStart, CallDurationSec, CallDestination, CallType, ItemName, OrderID FROM CallUsage")
        rows = cursor.fetchall()
        unique_orders = set()

        exsited_service = ExsitedService()
        order_service = OrderService(exsited_service)

        for row in rows:
            call_id, call_start, call_duration, call_destination, call_type, item_name, order_id = row
            unique_orders.add((order_id, item_name))

        charge_item_uuids = {}
        for order_id, item_name in unique_orders:
            charge_item_uuid = order_service.get_charge_item_uuid_by_order_id(order_id, item_name)
            charge_item_uuids[(order_id, item_name)] = charge_item_uuid

        call_usage_list = []
        unique_orders = set()

        for row in rows:
            call_id, call_start, call_duration, call_destination, call_type, item_name, order_id = row
            call_end = call_start + timedelta(seconds=call_duration)
            charging_period = calculate_charging_period(call_start)

            call_usage_data = create_usage_dto(charge_item_uuid=charge_item_uuids[(order_id, item_name)], quantity="1",
                                               start_time=call_start.strftime('%Y-%m-%d %H:%M:%S'),
                                               end_time=call_end.strftime('%Y-%m-%d %H:%M:%S'),
                                               charging_period=charging_period)

            response = order_service.order_usage_add(call_usage_data)
            call_usage_entry = {
                "charge_item_uuid": charge_item_uuids[(order_id, item_name)],
                "quantity": 1,
                "start_time": call_start.strftime('%Y-%m-%d %H:%M:%S'),
                "end_time": call_end.strftime('%Y-%m-%d %H:%M:%S'),
                "type": "INCREMENTAL",
                "charging_period": charging_period,
                "response": response
            }

            call_usage_list.append(call_usage_entry)

        return call_usage_list

    finally:
        cursor.close()
        db.close()


def fetch_message_usage():
    db = connect_to_db()
    cursor = db.cursor()

    try:
        cursor.execute("SELECT ID, BillingPeriod, BillableMessages, ItemName, OrderID FROM MessageUsage")
        rows = cursor.fetchall()
        unique_orders = set()

        exsited_service = ExsitedService()
        order_service = OrderService(exsited_service)

        for row in rows:
            message_id, billing_period, billable_messages, item_name, order_id = row
            unique_orders.add((order_id, item_name))

        charge_item_uuids = {}
        for order_id, item_name in unique_orders:
            charge_item_uuid = order_service.get_charge_item_uuid_by_order_id(order_id, item_name)
            charge_item_uuids[(order_id, item_name)] = charge_item_uuid

        message_usage_list = []
        for row in rows:
            message_id, billing_period, billable_messages, item_name, order_id = row
            charging_period = calculate_charging_period(billing_period)

            message_usage_data = create_usage_dto(charge_item_uuid=charge_item_uuids[(order_id, item_name)],
                                                  quantity=str(billable_messages),
                                                  start_time=billing_period.strftime('%Y-%m-%d %H:%M:%S'),
                                                  end_time=datetime(
                                                      billing_period.year,
                                                      billing_period.month,
                                                      billing_period.day,
                                                      23, 59, 59
                                                  ).strftime('%Y-%m-%d %H:%M:%S'),
                                                  charging_period=charging_period)
            response = order_service.order_usage_add(message_usage_data)

            message_usage_entry = {
                "charge_item_uuid": charge_item_uuids[(order_id, item_name)],
                "quantity": billable_messages,
                "start_time": billing_period.strftime('%Y-%m-%d %H:%M:%S'),
                "end_time": billing_period.strftime('%Y-%m-%d %H:%M:%S'),
                "type": "INCREMENTAL",
                "charging_period": charging_period,
                "response": response
            }

            message_usage_list.append(message_usage_entry)

        return message_usage_list

    finally:
        cursor.close()
        db.close()
