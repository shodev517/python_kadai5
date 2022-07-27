from ast import Not
import csv
import datetime
from logging import NullHandler
import eel

now = datetime.datetime.now()
filename = './receipt/' + now.strftime('%Y%m%d_%H%M%S') + '.txt'
path =(filename)


### 商品クラス
class Item:
    def __init__(self,item_code,item_name,price):
        self.item_code=item_code
        self.item_name=item_name
        self.price=price
    
    def get_price(self):
        return self.price


### オーダークラス
class Order(Item):
    # コンストラクタ
    def __init__(self,item_master):
        self.item_order_list=[]
        self.item_cnt_list=[]
        self.item_master=item_master
        self.total_price = 0
    
    # 商品注文
    def add_item_order(self, item_code, item_cnt):
        self.item_order_list.append(item_code)
        self.item_cnt_list.append(int(item_cnt))
        
    # オーダー一覧表示
    def view_item_list(self):
        
        self.total_price=0
        result_flg=True
        result=None
        
        # 画面クリア
        self.clear_display()
        
        # 合計金額算出
        num_cnt=0
        for item_code,item_cnt in zip(self.item_order_list, self.item_cnt_list):
            # オーダー番号から商品名、価格情報取得
            result = self.get_item_order(item_code)
            if result == None:
                result_flg = False
                del self.item_order_list[num_cnt]
                del self.item_cnt_list[num_cnt]
                break
            
            # 合計金額算出
            self.total_amount(result,item_cnt)
            
            # オーダー一覧出力
            self.write_receipt("商品コード:{}".format(item_code)+"　商品名：{}".format(result[0])+"　価格：{}円　".format(result[1])+"個数：{}".format(item_cnt))
            eel.view_order_log_js("商品コード:{}".format(item_code)+"　商品名：{}".format(result[0])+"　価格：{}円　".format(result[1])+"個数：{}".format(item_cnt))
            
            num_cnt += 1
        
        if result_flg == True:
            self.write_receipt("---------------------------------------------------------")
            eel.view_order_log_js("---------------------------------------------------------")
            self.write_receipt("合計金額は{}円です。".format(self.total_price)+"\n")
            eel.view_order_log_js("合計金額は{}円です。".format(self.total_price)+"\n")
        
    # オーダー番号から商品情報を取得        
    def get_item_order(self, item_code):
        for i in self.item_master:
            if item_code == i.item_code:
                return i.item_name, i.price
        eel.view_order_log_js("お取り扱いのない商品です。")
        
    # 合計金額算出
    def total_amount(self, result, item_cnt):
        self.total_price += int(result[1])*int(item_cnt)
                    
    # 会計
    def order_payment(self, input_money):
        self.write_receipt("{}円お預かりしました。".format(input_money)+"\n")
        eel.view_total_log_js("{}円お預かりしました。".format(input_money)+"\n")
        if int(input_money) >= self.total_price:
            change_money = int(input_money) - self.total_price
            self.write_receipt("おつりは{}円です。".format(change_money))
            eel.view_total_log_js("おつりは{}円です。".format(change_money)+"\n")
        else :
            change_money = self.total_price - int(input_money)
            print("金額が{}円足りません。".format(change_money))
            eel.view_total_log_js("金額が{}円足りません。再度お支払い金額を入力してください。".format(change_money))
            
    # レシート発行
    def write_receipt(self, text):
        print(text)
        # レシートに書き込み
        with open(path, mode='a', encoding='utf-8', newline="\n") as f:
                f.write(text)
                
    # 画面クリア
    def clear_display(self):
        eel.view_order_log_js_clear()

        
### メイン処理
class PosSystem:
    
    # コンストラクタ
    def __init__(self):
        self.item_master=[]
        self.order=None
        
    # 商品マスタ登録
    def register_master(self):
        csv_file = open("./master_list.csv", "r", encoding="utf-8", errors="", newline="" )
        f = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)    
        for row in f:
            self.item_master.append(Item(row[0],row[1],row[2]))

    # オーダー登録
    def init_order(self):
        self.order=Order(self.item_master)