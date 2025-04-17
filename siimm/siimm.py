from datetime import datetime
import requests
import load
from constants import (
    URL_FIRST_STEP,
    TIMEOUT,
    BASE_CONTENT_TYPE,
    USER_AGENT
)
from anticaptcha.recaptcha_v2 import RecaptchaSolved
from consumer import consumer_requests

class ProcessData:
    """Process entries params"""
    def __init__(self, numero_processo: str, numero_secretaria: str="6500", ano: str="2024"):
        self._numero_secretaria = numero_secretaria
        self._numero_processo = numero_processo
        self._ano = ano

    def get_process_data(self, attempts = 5):
        """Get processes data"""
        for attempt in range(attempts):
            try:
                # First Step
                cookie = consumer_requests.get_first_step_cookie()

                # Second Step
                payload_step_02 = (
                    f"javax.faces.partial.ajax=true&"
                    f"javax.faces.source=frm1%3AbtnPorCodigo&"
                    f"javax.faces.partial.execute=%40all&"
                    f"javax.faces.partial.render=frm1%3Agrowl&"
                    f"frm1%3AbtnPorCodigo=frm1%3AbtnPorCodigo&"
                    f"frm1=frm1&"
                    f"frm1%3Asecretaria={self._numero_secretaria}&"
                    f"frm1%3Anumero={self._numero_processo}&"
                    f"frm1%3Aano={self._ano}&"
                    f"g-recaptcha-response=&"
                )

                headers_step_02_03 = {
                'content-type': BASE_CONTENT_TYPE,
                'cookie': f'JSESSIONID={cookie};',
                'user-agent': USER_AGENT
                }

                response_02 = requests.request(method="POST",
                                                url=URL_FIRST_STEP,
                                                headers=headers_step_02_03,
                                                data=payload_step_02,
                                                timeout=TIMEOUT)
                javax = response_02.text.split("CDATA")[2].split("></update></changes></partial-response>")[0].replace("[", "").replace("]", "")

                # Third step
                anticaptcha_key = RecaptchaSolved()
                anticaptcha_solved = anticaptcha_key.recaptcha_solved()

                payload_step_03 = (
                    f"javax.faces.partial.ajax=true&"
                    f"javax.faces.source=frm1%3AbtnPorCodigo&"
                    f"javax.faces.partial.execute=%40all&"
                    f"javax.faces.partial.render=frm1%3Agrowl&"
                    f"frm1%3AbtnPorCodigo=frm1%3AbtnPorCodigo&"
                    f"frm1=frm1&"
                    f"frm1%3Asecretaria={self._numero_secretaria}&"
                    f"frm1%3Anumero={self._numero_processo}&"
                    f"frm1%3Aano={self._ano}&"
                    f"g-recaptcha-response={anticaptcha_solved}&"
                    f"javax.faces.ViewState={javax}"
                )

                headers_step_02_03 = {
                'content-type': BASE_CONTENT_TYPE,
                'cookie': f'JSESSIONID={cookie};',
                'user-agent': USER_AGENT
                }

                response_03 = requests.request(method="POST",
                                                url=URL_FIRST_STEP,
                                                headers=headers_step_02_03,
                                                data=payload_step_03,
                                                timeout=TIMEOUT)
                if "redirect" not in response_03.text:
                    anticaptcha_key.incorrect_recaptcha()
                    raise ValueError("anticaptcha error")
                anticaptcha_key.correct_recaptcha()

                # Fourth step
                new_javax = consumer_requests.get_fourth_step_new_javax(
                    cookie=cookie
                )
                # Fifth step
                list_entries = consumer_requests.get_fifth_step_list_entries(
                    cookie=cookie,
                    new_javax=new_javax
                )
                load.to_json(
                    data={"data": [dict(data) for data in list_entries]},
                    base_folder=f"data/{datetime.now().strftime('%Y-%m-%d')}",
                    file_name=f"{self._numero_processo}.json"
                )
                print('Processo criado!!!')
                break
            except:
                print(f"number of attempt: {attempt}")
