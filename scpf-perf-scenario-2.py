from locust import task, between, LoadTestShape, constant
from locust.contrib.fasthttp import FastHttpUser
import LocustUtil as Util

device_instance = {}  # keep the status of device instance


# The instance of HttpUser can represent one sensor/device.
class WindSensor(FastHttpUser):
    wait_time = constant(1)

    # instance of task can represent one type. (One device may send various data)
    @task
    def post_input(self):

        # retrieve the dev instance
        dev_id = Util.get_id(self, "dev")
        if dev_id in device_instance:
            dev = device_instance[dev_id]
        else:
            dev = Util.get_simple_random_sensor_data(init_value=20, min=0, max=50, increment=10, error_rate=0.1)
#            dev.set_failure_rate(20, 10)
            device_instance[dev_id] = dev

        # create json data
        json_data = {
            "id": dev_id,
            "value": dev.next_int(),
            "seq": dev.get_message_seq(),
            "time": Util.get_current_time()
        }
        padded_json_data = Util.get_json_with_size(json_data, 1000)

        Util.wait_until_xth_second(60)

        # send data to target
        response = self.client.post(
            path="/api/v1/resources/topics//locust/scenario/1",
            data=padded_json_data,
            auth=None,
            headers={"Authorization": "Bearer {}".format(Util.get_access_token()),
                     "Content-Type": "application/json"},
            name=Util.get_class_name(self)
        )


class TemperatureSensor(FastHttpUser):
    wait_time = constant(1)

    # instance of task can represent one type. (One device may send various data)
    @task
    def post_input(self):

        # retrieve the dev instance
        dev_id = Util.get_id(self, "dev")
        if dev_id in device_instance:
            dev = device_instance[dev_id]
        else:
            dev = Util.get_cyclic_random_sensor_data(init_elapsed_time=0, period=300, min=-10, max=45, error_rate=0.1)
            device_instance[dev_id] = dev

        json_data = {
            "id": Util.get_id(self, "dev"),
            "value": dev.next_value(),
            "seq": dev.get_message_seq(),
            "time": Util.get_current_time()
        }
        padded_json_data = Util.get_json_with_size(json_data, 1000)
        Util.wait_until_xth_second(60)

        response = self.client.post(
            path="/api/v1/resources/topics//locust/scenario/2",
            data=padded_json_data,
            auth=None,
            headers={"Authorization": "Bearer {}".format(Util.get_access_token()),
                     "Content-Type": "application/json"},
            name=Util.get_class_name(self)
        )


class BatterySensor(FastHttpUser):
    wait_time = constant(1)

    # instance of task can represent one type. (One device may send various data)
    @task
    def post_input(self):

        # retrieve the dev instance
        dev_id = Util.get_id(self, "dev")
        if dev_id in device_instance:
            dev = device_instance[dev_id]
        else:
            dev = Util.get_diminishing_random_sensor_data(init_value=100, half_life_time=30, restart_time=120, error_rate=0.01)
            device_instance[dev_id] = dev

        json_data = {
            "id": Util.get_id(self, "dev"),   # "dev-xxxxx-n"
            "value": dev.next_value(),
            "seq": dev.get_message_seq(),
            "time": Util.get_current_time()
        }
        padded_json_data = Util.get_json_with_size(json_data, 1000)
        Util.wait_until_xth_second(60)

        response = self.client.post(
            path="/api/v1/resources/topics//locust/scenario/3",
            data=padded_json_data,
            auth=None,
            headers={"Authorization": "Bearer {}".format(Util.get_access_token()),
                     "Content-Type": "application/json"},
            name=Util.get_class_name(self)
        )

#        print(response.request.headers)
#       print("{}".format(json_data))

