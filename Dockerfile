# Use a base image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copiar apenas requirements.txt primeiro para cache eficiente
COPY requirements.txt .

# Atualizar pip e instalar dependências do projeto
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Agora copiar os outros arquivos
COPY . .

# Expor a porta
EXPOSE 8000

# Definir comando de execução
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
