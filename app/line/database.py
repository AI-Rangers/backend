import firebase_admin 
from firebase_admin import credentials 
from firebase_admin import firestore 
from pathlib import Path
from datetime import date
from . import config

firebase_key = config.SERVICE_ACCOUNT_KEY

print("載入KEY的Path", Path(f"{firebase_key}").absolute())

cred = credentials.Certificate(f"{firebase_key}")
firebase_admin.initialize_app(cred)
db = firestore.client()


# 批次結算
def batch_update_mission(doc_key):
    col = u'mission'
    # Collection Reference
    col_ref = db.collection(col)
    doc_ref_generator = col_ref.where(
        u'PartitionKey', u'==', doc_key).where(
            u'CalcDate', u'==', '').stream()

    # 結算日
    calc_date = date.today().strftime('%Y-%m-%d')
    field_updates = {u'CalcDate': calc_date}

    batch = db.batch()
    for doc_ref in doc_ref_generator:
        # Document Reference
        doc = col_ref.document(doc_ref.id)
        batch.update(doc, field_updates)
    batch.commit()

def get_mission(doc_key):
    # entities = repo.get(f"PartitionKey eq '{message_request.user_id}' and CalcDate eq ''")
    print("Get mission", doc_key) 
    doc_query = db.collection(u'mission').where(
        u'PartitionKey', u'==', doc_key).where(
            u'CalcDate', u'==', '').stream()

    list = []
    for doc in doc_query:
        list.append(doc.to_dict())
        print(u'{} => {}'.format(doc.id, doc.to_dict()))

    return list


def update_mission(mission):
    # mission = {
        # u'PartitionKey': message_request.user_id,
        # u'RowKey': str(uuid.uuid1()),
        # u'Result': result,
        # u'CalcDate': ''
    # }
    # doc = member
    # doc_ref = db.collection(u'mission').document(mission[u'PartitionKey'])
    col_ref = db.collection(u'mission')
    col_ref.add(mission)
    # doc_ref.set(mission)
    print("col_ref.id", col_ref.id)
    # print("doc_ref.id", doc_ref.id) 
    print("Add mission", mission) 


def exists_member(doc_key):
    # {
    #     'PartitionKey': 'users',
    #     'RowKey': 'Ue563aff03e86cdf9fd457d38671edfe1',
    #     'DisplayName': 'andy',
    #     'CurrentIntent': ''
    # }
    doc_ref = db.collection(u'members').document(doc_key)
    # query = cities_ref.where(u'capital', u'==', True)
    doc = doc_ref.get()
    if doc.exists:
        print(f'Document data: {doc.to_dict()}')
        return doc.to_dict()
    else:
        print(u'No such document!')
        return []


def add_money(member):
    col_ref = db.collection(u'members')
    doc_ref = col_ref.document(member[u'RowKey'])
    doc = col_ref.document(doc_ref.id)

    field_updates = {u'money': member[u'money']}
    doc.update(field_updates)
    print("doc_ref.id", doc_ref.id)
    # print("add money", doc.to_dict())

def update_money(doc_key: str, amount: int):
    col_ref = db.collection(u'members')
    doc_ref_generator = col_ref.where(u'RowKey', u'==', doc_key).stream()

    field_updates = {u'money': amount}

    for doc_ref in doc_ref_generator:
        doc_ref.reference.update(field_updates)

    # docs = list(posts_ref.where('slug', '==', post['slug']).stream())
    doc_ref = col_ref.document(doc_key)
    # print("doc_ref.id", doc_ref.id)
    doc = doc_ref.get()
    if doc.exists:
        print(f'Document data: {doc.to_dict()}')
        data = doc.to_dict()
        return data[u'money']
    else:
        print(u'No such document!')
        return None


def update_member(member):
    # doc = {
    #     u'PartitionKey': 'users',
    #     u'RowKey': user_id,
    #     u'DisplayName': profile.display_name,
    #     u'CurrentIntent': ''
    # }
    # doc = member
    doc_ref = db.collection(u'members').document(member[u'RowKey'])
    doc_ref.set(member)
    print("doc_ref.id", doc_ref.id) 
    print("Update Member", member) 

    # print("user_id", user_id) 

    # docs2 = db.collection(u'Q1').where(u'uid', u'==', user_id).stream()
    # print("docs2", docs2) 
    # doc = docs2.get()
    # print('Get Doc', 'uid => {}'.format(doc.to_dict()['uid']))



    # docs2 = db.collection(u'Q1').where(u'uid', u'==', 2).orderBy(`field`).stream()
    # print("docs2", docs2) 
    # for doc in docs2:
    #     print(u'{} => {}'.format(doc.id, doc.to_dict()))



    # entities = repo.get(f"RowKey eq '{user_id}'")
    # doc = {
    #     'name': "帽子",
    #     'email': "abc@gmail.com"
    # }

    # collection_ref = db.collection("member")
    # collection_ref.add(doc)
    # print("doc", doc)
    # print("collection_ref.id", collection_ref.id)

    # doc_ref = db.collection(u'Q1').document(u'DOC1')
    # my_data = {"uid": 2, "姓名": "value2"}
    # doc_ref.set(my_data)
    # print("doc_ref.id", doc_ref.id) 
    # DOC1

    # doc_ref2 = db.collection(u'Q1')
    # query_ref = doc_ref2.where(u'uid', u'==', 1)
    # docs2 = db.collection(u'Q1').where(u'uid', u'==', 2).stream()
    # print("docs2", docs2) 
    # for doc in docs2:
    #     print(u'{} => {}'.format(doc.id, doc.to_dict()))


    ########################################################################
    # collectio為集合，document為要寫入的文件
    # student1 = db.collection('Q1').document('DOC1')
    # student1.set({
    #     '姓名': '西野',
    #     '年齡': '23',
    #     '學號': '123456789'
    # })

# 	// 將 document 實例的資料取出來
#   const userSnapshot = await getDoc(userDocRef);
#   console.log(userSnapshot);
#   console.log(userSnapshot.exists());


    # 用來提醒自己已經新增好資料
    print('Done')

def get_member():
    #Get Collection
    doc_ref = db.collection('Q1')
    docs = doc_ref.get()
    print('Get Collection')
    for doc in docs:
        print(u'{} => {}'.format(doc.id, doc.to_dict()))
        # print(u'{} => {}'.format(doc.id, doc.to_dict()))

    #Get Doc
    doc_ref = db.collection('Q1').document('DOC1')
    docs = doc_ref.get()
    print('Get Doc', '姓名 => {}'.format(doc.to_dict()['姓名']))
    print('Get Doc', '年齡 => {}'.format(doc.to_dict()['年齡']))

    #Get Doc
    doc_ref = db.collection('Q1').document('DOC2')
    docs = doc_ref.get()
    print('Get Doc2', '姓名 => {}'.format(doc.to_dict()['姓名']))
    print('Get Doc2', '年齡 => {}'.format(doc.to_dict()['年齡']))

    # print('姓名 => {}'.format(doc.to_dict()['姓名']))
    # print('年紀 => {}'.format(doc.to_dict()['年紀']))
    # print('工作 => {}'.format(doc.to_dict()['工作']))

