log_erros = []

def adicionar_erro_log(erro):
    log_erros.append(erro)

def mostrar_log_erros():
    if log_erros:
        return "\n".join(log_erros)
    else:
        return "Nenhum erro registrado."
