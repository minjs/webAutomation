from Emailer import Emailer

if __name__ == "__main__":
    email = Emailer()
    receiver = "renmin21cn@yahoo.com"
    dealDetail = {
        "brand": "kate spade",
        "description": "kate spade surprise sale",
        "hashcode": hash("kate spade surprise sale"),
        "link": "https://dealsea.com/view-deal/827333 ",
    }
    email.sendemail(dealDetail, receiver)