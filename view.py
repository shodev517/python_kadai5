from os import system
import sys
import eel
import desktop
from pos_system import PosSystem

app_name="html"
end_point="index.html"
size=(700,600)

@ eel.expose
def register_order(item_code, item_cnt):    
    # Orderインスタンスが存在するか確認し、なければインスタンス化
    if system.order == None:
        system.init_order()
        #print("init_order")
    
    # オーダー登録
    system.order.add_item_order(item_code, item_cnt)
    system.order.view_item_list()
    
@ eel.expose
def order_payment(input_money):
    system.order.order_payment(input_money)
    
@ eel.expose
def clear_order():
    init_pos_system()
    
def init_pos_system():
    '''
    POSシステムの初期化処理
    '''
    global system # グローバル変数を使用する場合の宣言
    
    # PosSystemインスタンス化
    system = PosSystem()
    
    # 商品マスタ登録
    system.register_master()
    
    # CSVインポートでマスタ登録する場合
    #system = PosSystem(ITEM_MASTER_CSV_PATH)
    #system.add_item_master() # CSVからマスタへ登録
    
if __name__ == "__main__":
    init_pos_system()
    desktop.start(app_name,end_point,size)