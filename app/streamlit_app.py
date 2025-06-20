import streamlit as st
import requests

BASE_URL = "http://app:8080"

# Сессия для хранения токена
if "token" not in st.session_state:
    st.session_state["token"] = None
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None

st.title("💳 Wine Quality Prediction App$")

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

# Предсказание фродовости транзакции
def predict():
    st.subheader("Предсказание фродовости транзакции")
    TransactionID = st.number_input('TransactionID')
    id_01 = st.number_input('id_01')
    id_02 = st.number_input('id_02')
    id_03 = st.number_input('id_03')
    id_04 = st.number_input('id_04')
    id_05 = st.number_input('id_05')
    id_06 = st.number_input('id_06')
    id_07 = st.number_input('id_07')
    id_08 = st.number_input('id_08')
    id_09 = st.number_input('id_09')
    id_10 = st.number_input('id_10')
    id_11 = st.number_input('id_11')
    id_12 = st.text_input('id_12')
    id_13 = st.number_input('id_13')
    id_14 = st.number_input('id_14')
    id_15 = st.text_input('id_15')
    id_16 = st.text_input('id_16')
    id_17 = st.number_input('id_17')
    id_18 = st.number_input('id_18')
    id_19 = st.number_input('id_19')
    id_20 = st.number_input('id_20')
    id_21 = st.number_input('id_21')
    id_22 = st.number_input('id_22')
    id_23 = st.text_input('id_23')
    id_24 = st.number_input('id_24')
    id_25 = st.number_input('id_25')
    id_26 = st.number_input('id_26')
    id_27 = st.text_input('id_27')
    id_28 = st.text_input('id_28')
    id_29 = st.text_input('id_29')
    id_30 = st.text_input('id_30')
    id_31 = st.text_input('id_31')
    id_32 = st.number_input('id_32')
    id_33 = st.text_input('id_33')
    id_34 = st.text_input('id_34')
    id_35 = st.text_input('id_35')
    id_36 = st.text_input('id_36')
    id_37 = st.text_input('id_37')
    id_38 = st.text_input('id_38')
    DeviceType = st.text_input('DeviceType')
    DeviceInfo = st.text_input('DeviceInfo')
    TransactionDT = st.number_input('TransactionDT')
    TransactionAmt = st.number_input('TransactionAmt')
    ProductCD = st.text_input('ProductCD')
    card1 = st.number_input('card1')
    card2 = st.number_input('card2')
    card3 = st.number_input('card3')
    card4 = st.text_input('card4')
    card5 = st.number_input('card5')
    card6 = st.text_input('card6')
    addr1 = st.number_input('addr1')
    addr2 = st.number_input('addr2')
    dist1 = st.number_input('dist1')
    dist2 = st.number_input('dist2')
    P_emaildomain = st.text_input('P_emaildomain')
    R_emaildomain = st.text_input('R_emaildomain')
    C1 = st.number_input('C1')
    C2 = st.number_input('C2')
    C3 = st.number_input('C3')
    C4 = st.number_input('C4')
    C5 = st.number_input('C5')
    C6 = st.number_input('C6')
    C7 = st.number_input('C7')
    C8 = st.number_input('C8')
    C9 = st.number_input('C9')
    C10 = st.number_input('C10')
    C11 = st.number_input('C11')
    C12 = st.number_input('C12')
    C13 = st.number_input('C13')
    C14 = st.number_input('C14')
    D1 = st.number_input('D1')
    D2 = st.number_input('D2')
    D3 = st.number_input('D3')
    D4 = st.number_input('D4')
    D5 = st.number_input('D5')
    D6 = st.number_input('D6')
    D7 = st.number_input('D7')
    D8 = st.number_input('D8')
    D9 = st.number_input('D9')
    D10 = st.number_input('D10')
    D11 = st.number_input('D11')
    D12 = st.number_input('D12')
    D13 = st.number_input('D13')
    D14 = st.number_input('D14')
    D15 = st.number_input('D15')
    M1 = st.text_input('M1')
    M2 = st.text_input('M2')
    M3 = st.text_input('M3')
    M4 = st.text_input('M4')
    M5 = st.text_input('M5')
    M6 = st.text_input('M6')
    M7 = st.text_input('M7')
    M8 = st.text_input('M8')
    M9 = st.text_input('M9')
    V1 = st.number_input('V1')
    V2 = st.number_input('V2')
    V3 = st.number_input('V3')
    V4 = st.number_input('V4')
    V5 = st.number_input('V5')
    V6 = st.number_input('V6')
    V7 = st.number_input('V7')
    V8 = st.number_input('V8')
    V9 = st.number_input('V9')
    V10 = st.number_input('V10')
    V11 = st.number_input('V11')
    V12 = st.number_input('V12')
    V13 = st.number_input('V13')
    V14 = st.number_input('V14')
    V15 = st.number_input('V15')
    V16 = st.number_input('V16')
    V17 = st.number_input('V17')
    V18 = st.number_input('V18')
    V19 = st.number_input('V19')
    V20 = st.number_input('V20')
    V21 = st.number_input('V21')
    V22 = st.number_input('V22')
    V23 = st.number_input('V23')
    V24 = st.number_input('V24')
    V25 = st.number_input('V25')
    V26 = st.number_input('V26')
    V27 = st.number_input('V27')
    V28 = st.number_input('V28')
    V29 = st.number_input('V29')
    V30 = st.number_input('V30')
    V31 = st.number_input('V31')
    V32 = st.number_input('V32')
    V33 = st.number_input('V33')
    V34 = st.number_input('V34')
    V35 = st.number_input('V35')
    V36 = st.number_input('V36')
    V37 = st.number_input('V37')
    V38 = st.number_input('V38')
    V39 = st.number_input('V39')
    V40 = st.number_input('V40')
    V41 = st.number_input('V41')
    V42 = st.number_input('V42')
    V43 = st.number_input('V43')
    V44 = st.number_input('V44')
    V45 = st.number_input('V45')
    V46 = st.number_input('V46')
    V47 = st.number_input('V47')
    V48 = st.number_input('V48')
    V49 = st.number_input('V49')
    V50 = st.number_input('V50')
    V51 = st.number_input('V51')
    V52 = st.number_input('V52')
    V53 = st.number_input('V53')
    V54 = st.number_input('V54')
    V55 = st.number_input('V55')
    V56 = st.number_input('V56')
    V57 = st.number_input('V57')
    V58 = st.number_input('V58')
    V59 = st.number_input('V59')
    V60 = st.number_input('V60')
    V61 = st.number_input('V61')
    V62 = st.number_input('V62')
    V63 = st.number_input('V63')
    V64 = st.number_input('V64')
    V65 = st.number_input('V65')
    V66 = st.number_input('V66')
    V67 = st.number_input('V67')
    V68 = st.number_input('V68')
    V69 = st.number_input('V69')
    V70 = st.number_input('V70')
    V71 = st.number_input('V71')
    V72 = st.number_input('V72')
    V73 = st.number_input('V73')
    V74 = st.number_input('V74')
    V75 = st.number_input('V75')
    V76 = st.number_input('V76')
    V77 = st.number_input('V77')
    V78 = st.number_input('V78')
    V79 = st.number_input('V79')
    V80 = st.number_input('V80')
    V81 = st.number_input('V81')
    V82 = st.number_input('V82')
    V83 = st.number_input('V83')
    V84 = st.number_input('V84')
    V85 = st.number_input('V85')
    V86 = st.number_input('V86')
    V87 = st.number_input('V87')
    V88 = st.number_input('V88')
    V89 = st.number_input('V89')
    V90 = st.number_input('V90')
    V91 = st.number_input('V91')
    V92 = st.number_input('V92')
    V93 = st.number_input('V93')
    V94 = st.number_input('V94')
    V95 = st.number_input('V95')
    V96 = st.number_input('V96')
    V97 = st.number_input('V97')
    V98 = st.number_input('V98')
    V99 = st.number_input('V99')
    V100 = st.number_input('V100')
    V101 = st.number_input('V101')
    V102 = st.number_input('V102')
    V103 = st.number_input('V103')
    V104 = st.number_input('V104')
    V105 = st.number_input('V105')
    V106 = st.number_input('V106')
    V107 = st.number_input('V107')
    V108 = st.number_input('V108')
    V109 = st.number_input('V109')
    V110 = st.number_input('V110')
    V111 = st.number_input('V111')
    V112 = st.number_input('V112')
    V113 = st.number_input('V113')
    V114 = st.number_input('V114')
    V115 = st.number_input('V115')
    V116 = st.number_input('V116')
    V117 = st.number_input('V117')
    V118 = st.number_input('V118')
    V119 = st.number_input('V119')
    V120 = st.number_input('V120')
    V121 = st.number_input('V121')
    V122 = st.number_input('V122')
    V123 = st.number_input('V123')
    V124 = st.number_input('V124')
    V125 = st.number_input('V125')
    V126 = st.number_input('V126')
    V127 = st.number_input('V127')
    V128 = st.number_input('V128')
    V129 = st.number_input('V129')
    V130 = st.number_input('V130')
    V131 = st.number_input('V131')
    V132 = st.number_input('V132')
    V133 = st.number_input('V133')
    V134 = st.number_input('V134')
    V135 = st.number_input('V135')
    V136 = st.number_input('V136')
    V137 = st.number_input('V137')
    V138 = st.number_input('V138')
    V139 = st.number_input('V139')
    V140 = st.number_input('V140')
    V141 = st.number_input('V141')
    V142 = st.number_input('V142')
    V143 = st.number_input('V143')
    V144 = st.number_input('V144')
    V145 = st.number_input('V145')
    V146 = st.number_input('V146')
    V147 = st.number_input('V147')
    V148 = st.number_input('V148')
    V149 = st.number_input('V149')
    V150 = st.number_input('V150')
    V151 = st.number_input('V151')
    V152 = st.number_input('V152')
    V153 = st.number_input('V153')
    V154 = st.number_input('V154')
    V155 = st.number_input('V155')
    V156 = st.number_input('V156')
    V157 = st.number_input('V157')
    V158 = st.number_input('V158')
    V159 = st.number_input('V159')
    V160 = st.number_input('V160')
    V161 = st.number_input('V161')
    V162 = st.number_input('V162')
    V163 = st.number_input('V163')
    V164 = st.number_input('V164')
    V165 = st.number_input('V165')
    V166 = st.number_input('V166')
    V167 = st.number_input('V167')
    V168 = st.number_input('V168')
    V169 = st.number_input('V169')
    V170 = st.number_input('V170')
    V171 = st.number_input('V171')
    V172 = st.number_input('V172')
    V173 = st.number_input('V173')
    V174 = st.number_input('V174')
    V175 = st.number_input('V175')
    V176 = st.number_input('V176')
    V177 = st.number_input('V177')
    V178 = st.number_input('V178')
    V179 = st.number_input('V179')
    V180 = st.number_input('V180')
    V181 = st.number_input('V181')
    V182 = st.number_input('V182')
    V183 = st.number_input('V183')
    V184 = st.number_input('V184')
    V185 = st.number_input('V185')
    V186 = st.number_input('V186')
    V187 = st.number_input('V187')
    V188 = st.number_input('V188')
    V189 = st.number_input('V189')
    V190 = st.number_input('V190')
    V191 = st.number_input('V191')
    V192 = st.number_input('V192')
    V193 = st.number_input('V193')
    V194 = st.number_input('V194')
    V195 = st.number_input('V195')
    V196 = st.number_input('V196')
    V197 = st.number_input('V197')
    V198 = st.number_input('V198')
    V199 = st.number_input('V199')
    V200 = st.number_input('V200')
    V201 = st.number_input('V201')
    V202 = st.number_input('V202')
    V203 = st.number_input('V203')
    V204 = st.number_input('V204')
    V205 = st.number_input('V205')
    V206 = st.number_input('V206')
    V207 = st.number_input('V207')
    V208 = st.number_input('V208')
    V209 = st.number_input('V209')
    V210 = st.number_input('V210')
    V211 = st.number_input('V211')
    V212 = st.number_input('V212')
    V213 = st.number_input('V213')
    V214 = st.number_input('V214')
    V215 = st.number_input('V215')
    V216 = st.number_input('V216')
    V217 = st.number_input('V217')
    V218 = st.number_input('V218')
    V219 = st.number_input('V219')
    V220 = st.number_input('V220')
    V221 = st.number_input('V221')
    V222 = st.number_input('V222')
    V223 = st.number_input('V223')
    V224 = st.number_input('V224')
    V225 = st.number_input('V225')
    V226 = st.number_input('V226')
    V227 = st.number_input('V227')
    V228 = st.number_input('V228')
    V229 = st.number_input('V229')
    V230 = st.number_input('V230')
    V231 = st.number_input('V231')
    V232 = st.number_input('V232')
    V233 = st.number_input('V233')
    V234 = st.number_input('V234')
    V235 = st.number_input('V235')
    V236 = st.number_input('V236')
    V237 = st.number_input('V237')
    V238 = st.number_input('V238')
    V239 = st.number_input('V239')
    V240 = st.number_input('V240')
    V241 = st.number_input('V241')
    V242 = st.number_input('V242')
    V243 = st.number_input('V243')
    V244 = st.number_input('V244')
    V245 = st.number_input('V245')
    V246 = st.number_input('V246')
    V247 = st.number_input('V247')
    V248 = st.number_input('V248')
    V249 = st.number_input('V249')
    V250 = st.number_input('V250')
    V251 = st.number_input('V251')
    V252 = st.number_input('V252')
    V253 = st.number_input('V253')
    V254 = st.number_input('V254')
    V255 = st.number_input('V255')
    V256 = st.number_input('V256')
    V257 = st.number_input('V257')
    V258 = st.number_input('V258')
    V259 = st.number_input('V259')
    V260 = st.number_input('V260')
    V261 = st.number_input('V261')
    V262 = st.number_input('V262')
    V263 = st.number_input('V263')
    V264 = st.number_input('V264')
    V265 = st.number_input('V265')
    V266 = st.number_input('V266')
    V267 = st.number_input('V267')
    V268 = st.number_input('V268')
    V269 = st.number_input('V269')
    V270 = st.number_input('V270')
    V271 = st.number_input('V271')
    V272 = st.number_input('V272')
    V273 = st.number_input('V273')
    V274 = st.number_input('V274')
    V275 = st.number_input('V275')
    V276 = st.number_input('V276')
    V277 = st.number_input('V277')
    V278 = st.number_input('V278')
    V279 = st.number_input('V279')
    V280 = st.number_input('V280')
    V281 = st.number_input('V281')
    V282 = st.number_input('V282')
    V283 = st.number_input('V283')
    V284 = st.number_input('V284')
    V285 = st.number_input('V285')
    V286 = st.number_input('V286')
    V287 = st.number_input('V287')
    V288 = st.number_input('V288')
    V289 = st.number_input('V289')
    V290 = st.number_input('V290')
    V291 = st.number_input('V291')
    V292 = st.number_input('V292')
    V293 = st.number_input('V293')
    V294 = st.number_input('V294')
    V295 = st.number_input('V295')
    V296 = st.number_input('V296')
    V297 = st.number_input('V297')
    V298 = st.number_input('V298')
    V299 = st.number_input('V299')
    V300 = st.number_input('V300')
    V301 = st.number_input('V301')
    V302 = st.number_input('V302')
    V303 = st.number_input('V303')
    V304 = st.number_input('V304')
    V305 = st.number_input('V305')
    V306 = st.number_input('V306')
    V307 = st.number_input('V307')
    V308 = st.number_input('V308')
    V309 = st.number_input('V309')
    V310 = st.number_input('V310')
    V311 = st.number_input('V311')
    V312 = st.number_input('V312')
    V313 = st.number_input('V313')
    V314 = st.number_input('V314')
    V315 = st.number_input('V315')
    V316 = st.number_input('V316')
    V317 = st.number_input('V317')
    V318 = st.number_input('V318')
    V319 = st.number_input('V319')
    V320 = st.number_input('V320')
    V321 = st.number_input('V321')
    V322 = st.number_input('V322')
    V323 = st.number_input('V323')
    V324 = st.number_input('V324')
    V325 = st.number_input('V325')
    V326 = st.number_input('V326')
    V327 = st.number_input('V327')
    V328 = st.number_input('V328')
    V329 = st.number_input('V329')
    V330 = st.number_input('V330')
    V331 = st.number_input('V331')
    V332 = st.number_input('V332')
    V333 = st.number_input('V333')
    V334 = st.number_input('V334')
    V335 = st.number_input('V335')
    V336 = st.number_input('V336')
    V337 = st.number_input('V337')
    V338 = st.number_input('V338')
    V339 = st.number_input('V339')

    if st.button("Поставить задачу в очередь предсказаний"):
        if st.session_state["token"] :#and st.session_state["user_id"]:

            headers = {"Authorization": f"Bearer {st.session_state['token']}"}
            data = {
                'TransactionID': TransactionID,
                'id_01': id_01,
                'id_02': id_02,
                'id_03': id_03,
                'id_04': id_04,
                'id_05': id_05,
                'id_06': id_06,
                'id_07': id_07,
                'id_08': id_08,
                'id_09': id_09,
                'id_10': id_10,
                'id_11': id_11,
                'id_12': id_12,
                'id_13': id_13,
                'id_14': id_14,
                'id_15': id_15,
                'id_16': id_16,
                'id_17': id_17,
                'id_18': id_18,
                'id_19': id_19,
                'id_20': id_20,
                'id_21': id_21,
                'id_22': id_22,
                'id_23': id_23,
                'id_24': id_24,
                'id_25': id_25,
                'id_26': id_26,
                'id_27': id_27,
                'id_28': id_28,
                'id_29': id_29,
                'id_30': id_30,
                'id_31': id_31,
                'id_32': id_32,
                'id_33': id_33,
                'id_34': id_34,
                'id_35': id_35,
                'id_36': id_36,
                'id_37': id_37,
                'id_38': id_38,
                'DeviceType': DeviceType,
                'DeviceInfo': DeviceInfo,
                'TransactionDT': TransactionDT,
                'TransactionAmt': TransactionAmt,
                'ProductCD': ProductCD,
                'card1': card1,
                'card2': card2,
                'card3': card3,
                'card4': card4,
                'card5': card5,
                'card6': card6,
                'addr1': addr1,
                'addr2': addr2,
                'dist1': dist1,
                'dist2': dist2,
                'P_emaildomain': P_emaildomain,
                'R_emaildomain': R_emaildomain,
                'C1': C1,
                'C2': C2,
                'C3': C3,
                'C4': C4,
                'C5': C5,
                'C6': C6,
                'C7': C7,
                'C8': C8,
                'C9': C9,
                'C10': C10,
                'C11': C11,
                'C12': C12,
                'C13': C13,
                'C14': C14,
                'D1': D1,
                'D2': D2,
                'D3': D3,
                'D4': D4,
                'D5': D5,
                'D6': D6,
                'D7': D7,
                'D8': D8,
                'D9': D9,
                'D10': D10,
                'D11': D11,
                'D12': D12,
                'D13': D13,
                'D14': D14,
                'D15': D15,
                'M1': M1,
                'M2': M2,
                'M3': M3,
                'M4': M4,
                'M5': M5,
                'M6': M6,
                'M7': M7,
                'M8': M8,
                'M9': M9,
                'V1': V1,
                'V2': V2,
                'V3': V3,
                'V4': V4,
                'V5': V5,
                'V6': V6,
                'V7': V7,
                'V8': V8,
                'V9': V9,
                'V10': V10,
                'V11': V11,
                'V12': V12,
                'V13': V13,
                'V14': V14,
                'V15': V15,
                'V16': V16,
                'V17': V17,
                'V18': V18,
                'V19': V19,
                'V20': V20,
                'V21': V21,
                'V22': V22,
                'V23': V23,
                'V24': V24,
                'V25': V25,
                'V26': V26,
                'V27': V27,
                'V28': V28,
                'V29': V29,
                'V30': V30,
                'V31': V31,
                'V32': V32,
                'V33': V33,
                'V34': V34,
                'V35': V35,
                'V36': V36,
                'V37': V37,
                'V38': V38,
                'V39': V39,
                'V40': V40,
                'V41': V41,
                'V42': V42,
                'V43': V43,
                'V44': V44,
                'V45': V45,
                'V46': V46,
                'V47': V47,
                'V48': V48,
                'V49': V49,
                'V50': V50,
                'V51': V51,
                'V52': V52,
                'V53': V53,
                'V54': V54,
                'V55': V55,
                'V56': V56,
                'V57': V57,
                'V58': V58,
                'V59': V59,
                'V60': V60,
                'V61': V61,
                'V62': V62,
                'V63': V63,
                'V64': V64,
                'V65': V65,
                'V66': V66,
                'V67': V67,
                'V68': V68,
                'V69': V69,
                'V70': V70,
                'V71': V71,
                'V72': V72,
                'V73': V73,
                'V74': V74,
                'V75': V75,
                'V76': V76,
                'V77': V77,
                'V78': V78,
                'V79': V79,
                'V80': V80,
                'V81': V81,
                'V82': V82,
                'V83': V83,
                'V84': V84,
                'V85': V85,
                'V86': V86,
                'V87': V87,
                'V88': V88,
                'V89': V89,
                'V90': V90,
                'V91': V91,
                'V92': V92,
                'V93': V93,
                'V94': V94,
                'V95': V95,
                'V96': V96,
                'V97': V97,
                'V98': V98,
                'V99': V99,
                'V100': V100,
                'V101': V101,
                'V102': V102,
                'V103': V103,
                'V104': V104,
                'V105': V105,
                'V106': V106,
                'V107': V107,
                'V108': V108,
                'V109': V109,
                'V110': V110,
                'V111': V111,
                'V112': V112,
                'V113': V113,
                'V114': V114,
                'V115': V115,
                'V116': V116,
                'V117': V117,
                'V118': V118,
                'V119': V119,
                'V120': V120,
                'V121': V121,
                'V122': V122,
                'V123': V123,
                'V124': V124,
                'V125': V125,
                'V126': V126,
                'V127': V127,
                'V128': V128,
                'V129': V129,
                'V130': V130,
                'V131': V131,
                'V132': V132,
                'V133': V133,
                'V134': V134,
                'V135': V135,
                'V136': V136,
                'V137': V137,
                'V138': V138,
                'V139': V139,
                'V140': V140,
                'V141': V141,
                'V142': V142,
                'V143': V143,
                'V144': V144,
                'V145': V145,
                'V146': V146,
                'V147': V147,
                'V148': V148,
                'V149': V149,
                'V150': V150,
                'V151': V151,
                'V152': V152,
                'V153': V153,
                'V154': V154,
                'V155': V155,
                'V156': V156,
                'V157': V157,
                'V158': V158,
                'V159': V159,
                'V160': V160,
                'V161': V161,
                'V162': V162,
                'V163': V163,
                'V164': V164,
                'V165': V165,
                'V166': V166,
                'V167': V167,
                'V168': V168,
                'V169': V169,
                'V170': V170,
                'V171': V171,
                'V172': V172,
                'V173': V173,
                'V174': V174,
                'V175': V175,
                'V176': V176,
                'V177': V177,
                'V178': V178,
                'V179': V179,
                'V180': V180,
                'V181': V181,
                'V182': V182,
                'V183': V183,
                'V184': V184,
                'V185': V185,
                'V186': V186,
                'V187': V187,
                'V188': V188,
                'V189': V189,
                'V190': V190,
                'V191': V191,
                'V192': V192,
                'V193': V193,
                'V194': V194,
                'V195': V195,
                'V196': V196,
                'V197': V197,
                'V198': V198,
                'V199': V199,
                'V200': V200,
                'V201': V201,
                'V202': V202,
                'V203': V203,
                'V204': V204,
                'V205': V205,
                'V206': V206,
                'V207': V207,
                'V208': V208,
                'V209': V209,
                'V210': V210,
                'V211': V211,
                'V212': V212,
                'V213': V213,
                'V214': V214,
                'V215': V215,
                'V216': V216,
                'V217': V217,
                'V218': V218,
                'V219': V219,
                'V220': V220,
                'V221': V221,
                'V222': V222,
                'V223': V223,
                'V224': V224,
                'V225': V225,
                'V226': V226,
                'V227': V227,
                'V228': V228,
                'V229': V229,
                'V230': V230,
                'V231': V231,
                'V232': V232,
                'V233': V233,
                'V234': V234,
                'V235': V235,
                'V236': V236,
                'V237': V237,
                'V238': V238,
                'V239': V239,
                'V240': V240,
                'V241': V241,
                'V242': V242,
                'V243': V243,
                'V244': V244,
                'V245': V245,
                'V246': V246,
                'V247': V247,
                'V248': V248,
                'V249': V249,
                'V250': V250,
                'V251': V251,
                'V252': V252,
                'V253': V253,
                'V254': V254,
                'V255': V255,
                'V256': V256,
                'V257': V257,
                'V258': V258,
                'V259': V259,
                'V260': V260,
                'V261': V261,
                'V262': V262,
                'V263': V263,
                'V264': V264,
                'V265': V265,
                'V266': V266,
                'V267': V267,
                'V268': V268,
                'V269': V269,
                'V270': V270,
                'V271': V271,
                'V272': V272,
                'V273': V273,
                'V274': V274,
                'V275': V275,
                'V276': V276,
                'V277': V277,
                'V278': V278,
                'V279': V279,
                'V280': V280,
                'V281': V281,
                'V282': V282,
                'V283': V283,
                'V284': V284,
                'V285': V285,
                'V286': V286,
                'V287': V287,
                'V288': V288,
                'V289': V289,
                'V290': V290,
                'V291': V291,
                'V292': V292,
                'V293': V293,
                'V294': V294,
                'V295': V295,
                'V296': V296,
                'V297': V297,
                'V298': V298,
                'V299': V299,
                'V300': V300,
                'V301': V301,
                'V302': V302,
                'V303': V303,
                'V304': V304,
                'V305': V305,
                'V306': V306,
                'V307': V307,
                'V308': V308,
                'V309': V309,
                'V310': V310,
                'V311': V311,
                'V312': V312,
                'V313': V313,
                'V314': V314,
                'V315': V315,
                'V316': V316,
                'V317': V317,
                'V318': V318,
                'V319': V319,
                'V320': V320,
                'V321': V321,
                'V322': V322,
                'V323': V323,
                'V324': V324,
                'V325': V325,
                'V326': V326,
                'V327': V327,
                'V328': V328,
                'V329': V329,
                'V330': V330,
                'V331': V331,
                'V332': V332,
                'V333': V333,
                'V334': V334,
                'V335': V335,
                'V336': V336,
                'V337': V337,
                'V338': V338,
                'V339': V339,
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
