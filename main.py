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
URL_SITE = "https://filosofocomputacional.github.io/site/carometro"
SENHA_ACESSO = "8737"

def registrar_log(mensagem):
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linha_log = f"[{data_hora}] {mensagem}\n"
    
    print(linha_log.strip())
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(linha_log)

def executar_rotina():
    registrar_log("Iniciando execução da rotina...")
    
    # Configurações para rodar no servidor sem tela do GitHub
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
        
        # Clica no botão situado logo abaixo do input de senha
        botao_login = driver.find_element(By.XPATH, "//input[@id='login-password']/following::button[1]")
        botao_login.click()
        
        # 2. Selecionar Etapa de Ensino (aleatória)
        elem_etapa = wait.until(EC.presence_of_element_locator((By.ID, "select-etapa")))
        select_etapa = Select(elem_etapa)
        
        # Filtra apenas opções válidas (excluindo marcadores de posição/placeholders)
        opcoes_etapa = [opt for opt in select_etapa.options if opt.get_attribute("value") and opt.get_attribute("value").strip() != ""]
        if not opcoes_etapa:
            raise Exception("Nenhuma etapa disponível para seleção.")
        
        etapa_escolhida = random.choice(opcoes_etapa)
        nome_etapa = etapa_escolhida.text.strip()
        select_etapa.select_by_value(etapa_escolhida.get_attribute("value"))
        
        # Aguarda pequeno intervalo para carregamento das turmas vinculadas à etapa
        time.sleep(1)
        
        # 3. Selecionar Turma (aleatória)
        elem_turmas = wait.until(EC.presence_of_element_locator((By.ID, "select-turmas")))
        select_turmas = Select(elem_turmas)
        
        opcoes_turma = [opt for opt in select_turmas.options if opt.get_attribute("value") and opt.get_attribute("value").strip() != ""]
        if not opcoes_turma:
            raise Exception(f"Nenhuma turma encontrada para a etapa '{nome_etapa}'.")
            
        turma_escolhida = random.choice(opcoes_turma)
        nome_turma = turma_escolhida.text.strip()
        select_turmas.select_by_value(turma_escolhida.get_attribute("value"))
        
        # Registro de sucesso no arquivo de log
        registrar_log(f"CONSOLIDADO COM SUCESSO | Etapa: '{nome_etapa}' | Turma: '{nome_turma}'")

    except Exception as e:
        registrar_log(f"ERRO NA EXECUÇÃO: {str(e)}")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    # Executa a rotina uma única vez quando chamado pelo GitHub Actions
    executar_rotina()
