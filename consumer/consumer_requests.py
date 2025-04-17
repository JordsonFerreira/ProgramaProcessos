"""Consumer requests"""

from urllib.parse import quote
import requests
from selectolax.lexbor import LexborHTMLParser
from constants import (
    URL_FIRST_STEP,
    HEADERS_FIRST_STEP,
    TIMEOUT,
    USER_AGENT,
    BASE_CONTENT_TYPE
)
from schema import Atualizacao, ConsumerException


def get_first_step_cookie():
    """Get cookie to first step"""
    response_01 = requests.request(
        method="GET",
        url=URL_FIRST_STEP,
        headers=HEADERS_FIRST_STEP,
        timeout=TIMEOUT)

    if response_01.status_code == 200:
        cookie = response_01.cookies.get("JSESSIONID")
        return cookie
    raise ConsumerException(status_code=500,
                            message="First step service is not accessible or operational.")


def get_fourth_step_new_javax(cookie):
    """Get new javax to fourth step"""

    headers_04 = {
        'cookie': f'JSESSIONID={cookie};',
        'user-agent': USER_AGENT
    }

    url_fouth_step = "https://www3.siimm.maceio.al.gov.br/consultaprocesso/pages/detalhesprocesso.faces"
    response_04 = requests.request(
        method="GET",
        url=url_fouth_step,
        headers=headers_04
    )

    if response_04.status_code == 200:
        get_new_javax_value = LexborHTMLParser(response_04.text).css_first(
            "#j_id1\\:javax\\.faces\\.ViewState\\:0")
        if not get_new_javax_value:
            if not get_new_javax_value.attributes["value"]:  # type: ignore
                raise ValueError("get new javax value error")
        new_javax = quote(
            get_new_javax_value.attributes["value"])  # type: ignore

        return new_javax
    raise ConsumerException(status_code=500,
                            message="Fourth step service is not accessible or operational.")


def get_fifth_step_list_entries(cookie, new_javax):
    """Get list entries for fifth step"""

    headers_05 = {
        'content-type': BASE_CONTENT_TYPE,
        'cookie': f'JSESSIONID={cookie};',
        'user-agent': USER_AGENT
    }

    payload_step_05 = (
        f"javax.faces.partial.ajax=true&"
        f"javax.faces.source=frmPrincipal%3Atabela&"
        f"javax.faces.partial.execute=frmPrincipal%3Atabela&"
        f"javax.faces.partial.render=frmPrincipal%3Atabela&"
        f"frmPrincipal%3Atabela=frmPrincipal%3Atabela&"
        f"frmPrincipal%3Atabela_pagination=true&"
        f"frmPrincipal%3Atabela_first=0&"
        f"frmPrincipal%3Atabela_rows=100&"
        f"frmPrincipal%3Atabela_skipChildren=true&"
        f"frmPrincipal%3Atabela_encodeFeature=true&"
        f"frmPrincipal=frmPrincipal&"
        f"javax.faces.ViewState={new_javax}"
    )

    url_fouth_step = "https://www3.siimm.maceio.al.gov.br/consultaprocesso/pages/detalhesprocesso.faces"

    response_05 = requests.request(
        method="POST",
        url=url_fouth_step,
        headers=headers_05,
        data=payload_step_05,
        timeout=TIMEOUT
    )

    if response_05.status_code == 200:
        get_table_step_01 = response_05.text.split(
            "<![CDATA[")[1].split("tr>]]>")[0]
        get_table_step_02 = f"{get_table_step_01}tr>"
        list_entries_row = get_table_step_02.split("</td>")[:-1]

        list_entries: list[Atualizacao] = []
        for entry in list_entries_row:
            step_01 = entry.split("Secretaria: </label>")[1]
            secretaria_name = step_01.split("</div>")[0]
            step_02 = step_01.split("Setor: </label>")[1]
            setor_name = step_02.split("</div>")[0]
            step_03 = step_02.split(
                'Recebido em </label><span class="fonteForm">')[1]
            data_name = step_03.split("</span>")[0]
            list_info = {
                "secretaria": secretaria_name.strip(),
                "setor": setor_name.strip(),
                "data": data_name.strip()[0:10]
            }
            list_entries.append(
                Atualizacao(**list_info)
            )
        return list_entries
    raise ConsumerException(status_code=500,
                            message="Fifth step service is not accessible or operational.")
