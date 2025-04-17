from anticaptchaofficial.recaptchav2proxyless import *

class RecaptchaSolved:
    def __init__(self):
        self.solver = recaptchaV2Proxyless()
        self.solver.set_verbose(1)
        self.solver.set_key("dc30717fef0f6e4dfa1b4b8f322c4fd6")
        self.solver.set_website_url("https://www3.siimm.maceio.al.gov.br/consultaprocesso/pages/localizarprocesso.faces")
        self.solver.set_website_key("6LeZxSQbAAAAAMFV2cryWD4hm7yxrttHUUlcOqTx")

    def recaptcha_solved(self):
        self.solver.set_soft_id(0)

        g_response = self.solver.solve_and_return_solution()
        if g_response != 0:
            return g_response
        raise ValueError("recaptcha error")
        
    def incorrect_recaptcha(self):
        self.solver.report_incorrect_recaptcha()
    
    def correct_recaptcha(self):
        self.solver.report_correct_recaptcha()