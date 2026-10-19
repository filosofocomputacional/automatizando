import time
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

LOG_FILE = "log_acesso_carometro.txt"
ARQUIVO_SUCESSO = "acessos_sucesso.txt"
URL_SITE = "https://filosofocomputacional.github.io/site/carometro"
SENHA_ACESSO = "8737"

def registrar_log(mensagem):
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linha_log = f"[{data_hora}] {mensagem}\n"
    
    print(linha_log.strip())
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(linha_log)

def registrar_sucesso(etapa, turma):
    """Registra apenas execuções que foram concluídas com sucesso"""
    data_hora = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
    linha = f"[{data_hora}] Acesso bem-sucedido | Etapa: '{etapa}' | Turma: '{turma}'\n"
    
    with open(ARQUIVO_SUCESSO, "a", encoding="utf-8") as file:
        file.write(linha)
    print(f"[OK] Sucesso registrado em {ARQUIVO_SUCESSO}")

def executar_rotina():
    registrar_log("Iniciando execução da rotina...")
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 10)
    
    try:
        driver.get(URL_SITE)
        
        # 1. Preencher a senha e clicar no botão de login
        campo_senha = wait.until(EC.presence_of_element_locator((By.ID, "login-password")))
        campo_senha.clear()
        campo_senha.send_keys(SENHA_ACESSO)
        
        botao_login = driver.find_element(By.XPATH, "//input[@id='login-password']/following::button[1]")
        botao_login.click()
        
        # 2. Selecionar Etapa
        elem_etapa = wait.until(EC.presence_of_element_locator((By.ID, "select-etapa")))
        select_etapa = Select(elem_etapa)
        
        opcoes_etapa = [opt for opt in select_etapa.options if opt.get_attribute("value") and opt.get_attribute("value").strip() != ""]
        if not opcoes_etapa:
            raise Exception("Nenhuma etapa disponível para seleção.")
        
        etapa_escolhida = random.choice(opcoes_etapa)
        nome_etapa = etapa_escolhida.text.strip()
        select_etapa.select_by_value(etapa_escolhida.get_attribute("value"))
        
        time.sleep(1)
        
        # 3. Selecionar Turma
        elem_turmas = wait.until(EC.presence_of_element_locator((By.ID, "select-turmas")))
        select_turmas = Select(elem_turmas)
        
        opcoes_turma = [opt for opt in select_turmas.options if opt.get_attribute("value") and opt.get_attribute("value").strip() != ""]
        if not opcoes_turma:
            raise Exception(f"Nenhuma turma encontrada para a etapa '{nome_etapa}'.")
            
        turma_escolhida = random.choice(opcoes_turma)
        nome_turma = turma_escolhida.text.strip()
        select_turmas.select_by_value(turma_escolhida.get_attribute("value"))
        
        # Registra o log geral e o arquivo exclusivo de sucessos
        registrar_log(f"CONSOLIDADO COM SUCESSO | Etapa: '{nome_etapa}' | Turma: '{nome_turma}'")
        registrar_sucesso(nome_etapa, nome_turma)

    except Exception as e:
        registrar_log(f"ERRO NA EXECUÇÃO: {str(e)}")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    executar_rotina()
