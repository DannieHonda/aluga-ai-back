from decouple import config
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__, template_folder='template')

db_user = config('DB_USER')
db_password = config('DB_PASSWORD')
db_host = config('DB_HOST', default='localhost')
database = "locadoradb"

@app.route('/')
def index():
    try:
        # Create a connection
        conn = mysql.connector.connect(
            user=db_user,
            password=db_password,
            host=db_host,
            database=database
        )

        # Use the connection to execute queries
        cursor = conn.cursor()

        # Execute the desired select query
        query = """
        SELECT ca.descricao, model.descricao, car.descricao
        FROM modelo_carro model
        INNER JOIN marca_carro car ON car.idmarca=model.idmarca
        INNER JOIN carro ca ON ca.idmodelo=model.idmodelo
        WHERE 1 = 1
        """

        cursor.execute(query)

        # Fetch the results
        result = cursor.fetchall()

        # Close the connection
        cursor.close()
        conn.close()

        # Render the HTML template and pass the results for display
        return render_template('index.html', result=result)

    except mysql.connector.Error as error:
        print("Error connecting to the database:", error)
        return "Error connecting to the database"
    
@app.route('/listar_carros')
def listar_carros():
    try:
        # Criação da conexão
        conn = mysql.connector.connect(
             user=db_user,
            password=db_password,
            host=db_host,
            database=database
        )

        # Utilize a conexão para executar consultas
        cursor = conn.cursor()

        # Executar o select desejado
        query = """
        SELECT ca.descricao, model.descricao, car.descricao
        FROM modelo_carro model
        INNER JOIN marca_carro car ON car.idmarca=model.idmarca
        INNER JOIN carro ca ON ca.idmodelo=model.idmodelo
        """

        cursor.execute(query)

        # Obter os resultados
        result = cursor.fetchall()

        # Fechando a conexão
        cursor.close()
        conn.close()

        # Renderizar o template HTML e passar os resultados para exibição
        return render_template('listar_carros.html', result=result)

    except mysql.connector.Error as error:
        print("Erro ao conectar ao banco de dados:", error)
        return "Erro ao conectar ao banco de dados"
       

@app.route('/reservas', methods=['GET', 'POST'])
def reservas():
    if request.method == 'POST':
        try:
            # Create a connection
            conn = mysql.connector.connect(
               user=db_user,
            password=db_password,
            host=db_host,
            database=database
            )

            # Use the connection to execute the reservation insertion
            cursor = conn.cursor()

            nome_cliente = request.form['nome_cliente']
            data_retirada = request.form['data_retirada']
            data_devolucao = request.form['data_devolucao']
         
            insert_query = """
            INSERT INTO reserva_carro (data_retirada, data_devolucao)
            VALUES (%s, %s)
            """

            cursor.execute(insert_query, (data_retirada, data_devolucao))
            conn.commit()

            # Close the connection
            cursor.close()
            conn.close()

            # Redirect the user to the reservation completed page
            return redirect(url_for('reserva_concluida'))

        except mysql.connector.Error as error:
            print("Error connecting to the database:", error)
            return "Error connecting to the database"
    return render_template('reservas.html')

@app.route('/reserva_concluida')
def reserva_concluida():
    return "Reserva realizada com sucesso!"

@app.route('/filtrar', methods=['POST'])
def filtrar():
    try:
        # Create a connection
        conn = mysql.connector.connect(
           user=db_user,
            password=db_password,
            host=db_host,
            database=database
        )

        # Use the connection to execute queries
        cursor = conn.cursor()

        descricao = request.form['descricao']

        # Execute the select query with the filter
        query = """
        SELECT ca.descricao, model.descricao, car.descricao
        FROM modelo_carro model
        INNER JOIN marca_carro car ON car.idmarca=model.idmarca
        INNER JOIN carro ca ON ca.idmodelo=model.idmodelo
        WHERE car.descricao LIKE %s
        """

        cursor.execute(query, ('%' + descricao + '%',))

        # Fetch the filtered results
        result = cursor.fetchall()

        # Close the connection
        cursor.close()
        conn.close()

        # Render the HTML template with the filtered results
        return render_template('index.html', result=result)

    except mysql.connector.Error as error:
        print("Error connecting to the database:", error)
        return "Error connecting to the database"

if __name__ == '__main__':
    app.debug = True
    app.run(port=8080)
