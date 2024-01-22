import json
from flask import Flask, redirect, session, request, render_template
from flask_session import Session
from auth.auth import authorize
from auth.auth import oauth2callback
from customers.list_accessible_customers import list_accessible_customers
from ga_runner import REFRESH_ERROR
from customers.link_manager_to_client import link_manager_to_client
from customers.get_campaigns import get_campaigns
from customers.search_accounts import search_accounts
from customers.detect_niche import detect_niche
from customers.get_account_keywords import get_account_keywords

app = Flask(__name__)
app.secret_key = "SECRET KEY"


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/authorize')
def authorize_endpoint():
    auth_info = authorize()
    passthrough_val = auth_info["passthrough_val"]
    session["passthrough_val"] = passthrough_val
    url = auth_info["authorization_url"]
    return redirect(url)

@app.route('/getAccountKeywords')
def getAccountKeywords_endpoint():
    try:
        print(session)
        token = session.get("refresh_token")
        
        # login_customer_id = session.get("parent_customer_client_id")
        # account_id = session.get("customer_client_id")
        account_id = "4425735794"
        login_customer_id = "4006438585"

        get_account_keywords(token,account_id,login_customer_id)

    except Exception as ex: 
        return handleException(ex)
    
    
@app.route('/getCampaigns')
def getCampaigns_endpoint():
    try:
        token = session["refresh_token"]
        
        login_customer_id = session['parent_customer_client_id']
        account_id = session['customer_client_id']

        get_campaigns(token,account_id,login_customer_id)

    except Exception as ex: 
        return handleException(ex)


@app.route('/oauth2callback')
def oauth2callback_endpoint():
    passthrough_val = session["passthrough_val"]
    state = request.args.get("state")
    code = request.args.get("code")
    refresh_token = oauth2callback(passthrough_val, state, code)
    session["passthrough_val"] = ""
    session["refresh_token"] = refresh_token
    return redirect("http://127.0.0.1:5000/customers")

@app.route('/getRecommendations')
def getRecommendations_endpoint():
    token = session["refresh_token"]


@app.route('/detectNiche')
def detectNiche_endpoint():
    try:
        keyword1 = "body shop"

        keyword2 ="bumper repair"

        keyword3 = "auto detailing"

        keyword4 = "car tint"

        keyword5 = "auto care center"

        keyword6 = "car detailing"

        keyword7 = " auto damage repair"

        accountKeywords = [keyword1,keyword2,keyword3,keyword4,keyword5,keyword6,keyword7]

        account_id = "111-1111-111"
        detect_niche(accountKeywords,account_id)

    except Exception as ex: 
        return handleException(ex)

    
@app.route('/customers')
def customers_endpoint():
    token = session["refresh_token"]
    print(token)
    try:
        resource_names = list_accessible_customers(token)
        customer_ids = []
        for i in resource_names:
            a,customer_id = i.split("/")
            customer_ids.append(customer_id)
        return render_template('customers.html', data=customer_ids)

    except Exception as ex: 
        return handleException(ex)

@app.route('/assignToManager',methods = ['POST'])
def assignToManager_endpoint(): 
    try: 
        client_token = session["refresh_token"]
        manager_token = "1//0grpnJjVXepluCgYIARAAGBASNwF-L9IrMMvOpYmos8GBEJH_qIQSgOyTnd5hDARho2RFYhLpsaKS1TG3YIJvQvub7UhCUJlsr1E"
        manager_customer_id = "5813755274" 
        # resource_name = request.args.get("resourceNames")
        # a,customer_client_id = resource_name.split("/")
        print(request.form['parent_customer_client_id'])
        print(request.form['child_customer_client_id'])


        parent_customer_client_id = request.form['parent_customer_client_id']
        child_customer_client_id = request.form['child_customer_client_id']

        if(child_customer_client_id!=''):
            customer_client_id = child_customer_client_id
        else:
            customer_client_id = parent_customer_client_id

        session["customer_client_id"] = customer_client_id
        session['parent_customer_client_id'] = parent_customer_client_id

        print("Selected customer_client_id = "+session['customer_client_id'])
        print("Selected parent_customer_client_id = "+session['parent_customer_client_id'])

        
        result = link_manager_to_client(client_token,manager_token, manager_customer_id,customer_client_id,parent_customer_client_id)
        message = []
        if(result!=True):
            message.append("There was a Problem With Linking this account with managaer")
        ## Get Keywords From the Account
        accountKeywords = get_account_keywords(client_token,customer_client_id,parent_customer_client_id)
        
        if(len(accountKeywords)>0):
            #Detect Nichee
            nicheName = detect_niche(accountKeywords,customer_client_id)
        else:
            message.append("no keywords were found")

        lastNicheMatchedKeywords =0;
        lastMatchedNicheName =''
        for niche in nicheName:
            print(niche)
            matched_niche_keywords = int(niche['matched_keywords'])
            print(matched_niche_keywords)
            if lastNicheMatchedKeywords < matched_niche_keywords:
                 lastMatchedNicheName = niche['niche_name']
            
        all_the_data ={
            "messages": message,
            "accountKeywords" : accountKeywords,
            "nicheName" : lastMatchedNicheName,
            "account_number" : customer_client_id
        }
        
        return render_template('final.html',data=all_the_data)
    except Exception as ex: 
        return handleException(ex)

@app.route('/search')
def search_endpoint():
    try:
        client_token = session["refresh_token"]
        customer_id = request.args.get("CustomerId")
        term = request.args.get("term")
        search_result = search_accounts(client_token, term, customer_id)
        return json.dumps(search_result)
    except Exception as ex: 
        return handleException(ex)

def handleException(ex):
    error = str(ex)
    if (error == REFRESH_ERROR):
        return json.dumps({
            "code": 401,
            "name": "INVALID_REFRESH_TOKEN",
            "description": error
        })
    else:
        return json.dumps({
            "code": 500,
            "name": "INTERNAL_SERVER_ERROR",
            "description": error
        })

if __name__ == "__main__":
    app.run(debug=True)