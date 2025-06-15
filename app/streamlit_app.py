import streamlit as st
import requests

BASE_URL = "http://app:8080"

# Сессия для хранения токена
if "token" not in st.session_state:
    st.session_state["token"] = None
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None

st.title("🍷 Wine Quality Prediction App")

# Регистрация
def register():
    st.subheader("Регистрация")
    email = st.text_input("Почта пользователя")
    password = st.text_input("Пароль", type="password")
    if st.button("Зарегистрироваться"):
        response = requests.post(f"{BASE_URL}/user/signup", json={"email": email, "password": password})
        if response.status_code == 200 and response.json().get("message") == "User successfully registered!":  #.message == "User successfully registered!":
            st.success("✅ Регистрация успешна!")
        else:
            st.error("❌ Ошибка регистрации.")

# Авторизация
def login():
    st.subheader("Авторизация")
    email = st.text_input("Почта пользователя")
    password = st.text_input("Пароль", type="password")
    if st.button("Войти"):
        response = requests.post(f"{BASE_URL}/user/signin", json={"email": email, "password": password})
        if response.status_code == 200:
            st.session_state["token"] = response.json()["access_token"]
            st.success("✅ Успешный вход!")
        else:
            st.error("❌ Ошибка авторизации.")

# Детализация аккаунта
def get_account_details():
    st.subheader("Детализация аккаунта")
    if st.session_state["token"] : #and st.session_state["user_id"]:
        headers = {"Authorization": f"Bearer {st.session_state['token']}"}
        response = requests.get(f"{BASE_URL}/account/details/", headers=headers)
        if response.status_code == 200:
            st.write(f" Ваш user_id: {response.json()['user_id']}")
            st.write(f"💰 Ваш баланс: {response.json()['balance']} кредитов")
            st.write(f" Ваши транзакции: {response.json()['transactions']}")
        else:
            st.error("Ошибка загрузки детализации аккаунта.")
    else:
        st.warning("Сначала войдите в систему.")

# Пополнение баланса
def add_funds():
    st.subheader("Пополнение баланса")
    amount = st.number_input("amount", value=0, step=1)
    if st.session_state["token"] and amount !=0 :#and st.session_state["user_id"]:

        headers = {"Authorization": f"Bearer {st.session_state['token']}"}
        data = {"amount": amount}
        response = requests.post(f"{BASE_URL}/account/fund/",json=data, headers=headers)
        if response.status_code == 200:
            st.write(f"💰 Ваш баланс пополнен на: {amount} кредитов")
        else:
            st.error("Ошибка пополнения баланса.")
    else:
        st.warning("Сначала войдите в систему.")

# Предсказание качества вина
def predict():
    st.subheader("Предсказание качества вина")
    fixed_acidity = st.number_input("fixed acidity")
    volatile_acidity = st.number_input("volatile acidity")
    citric_acid = st.number_input("citric acid")
    residual_sugar = st.number_input("residual sugar")
    chlorides = st.number_input("chlorides")
    free_sulfur_dioxide = st.number_input("free sulfur dioxide")
    total_sulfur_dioxide = st.number_input("total sulfur dioxide")
    density = st.number_input("density")
    pH = st.number_input("pH")
    sulphates = st.number_input("sulphates")
    alcohol = st.number_input("alcohol")
    if st.button("Поставить задачу в очередь предсказаний"):
        if st.session_state["token"] :#and st.session_state["user_id"]:

            headers = {"Authorization": f"Bearer {st.session_state['token']}"}
            data = {
                      "fixed acidity": fixed_acidity,
                      "volatile acidity": volatile_acidity,
                      "citric acid": citric_acid,
                      "residual sugar": residual_sugar,
                      "chlorides": chlorides,
                      "free sulfur dioxide": free_sulfur_dioxide,
                      "total sulfur dioxide": total_sulfur_dioxide,
                      "density": density,
                      "pH": pH,
                      "sulphates": sulphates,
                      "alcohol": alcohol
            }
            response = requests.post(f"{BASE_URL}/model/predict/", json=data, headers=headers)
            if response.status_code == 200:
                st.success(f"🍷 Смотрите результат в истории задач или по id после обработки задачи. id задачи: {response.json()['task_id']}")
            else:
                st.error("Ошибка предсказания.")
        else:
            st.warning("Сначала войдите в систему.")

def history():
    st.subheader("История предсказаний")
    if st.session_state["token"] :#and st.session_state["user_id"]:
        headers = {"Authorization": f"Bearer {st.session_state['token']}"}
        response = requests.get(f"{BASE_URL}/model/history", headers=headers)
        if response.status_code == 200:
            history_data = response.json() #.json()["history"]
            #for entry in history_data:
                #st.write(f"{entry}")
            st.write(f"{history_data}")
        else:
            st.error("Ошибка загрузки истории предсказаний.")
    else:
        st.warning("Сначала войдите в систему.")

def get_task():
    st.subheader("Результат предсказания")
    task_id = st.text_input("task_id",value = '')
    if st.session_state["token"] and task_id != '':#and st.session_state["user_id"]:
        headers = {"Authorization": f"Bearer {st.session_state['token']}"}
        response = requests.get(f"{BASE_URL}/model/predictResult/{task_id}", headers=headers)
        if response.status_code == 200:
            history_data = response.json()
            for key,value in history_data.items():
                st.write(f"{key} = {value}")
        else:
            st.error("Ошибка загрузки результата предсказания.")
    else:
        st.warning("Сначала войдите в систему.")

# Навигация
menu = st.sidebar.selectbox("Меню", ["Регистрация", "Авторизация", "Детализация аккаунта", "Предсказание", "История предсказаний", "Пополнение баланса", "Результат предсказания"])
if menu == "Регистрация":
    register()
elif menu == "Авторизация":
    login()
elif menu == "Детализация аккаунта":
    get_account_details()
elif menu == "Предсказание":
    predict()
elif menu == "История предсказаний":
    history()
elif menu == "Результат предсказания":
    get_task()
elif menu == "Пополнение баланса":
    add_funds()
