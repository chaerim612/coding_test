## 음료수 자판기 
## 커피 : 500 / 콜라 : 1000 / 환타 : 1000 / 사이다 : 700
## 선결제 후선택 -> 거스름돈 but 더 살 수 있으면 살거냐고 물어봄
## 동전 : 100,10,50,500 / 지폐 : 1000
## 음료수 1이상 10개 이하 (난수 발생) random
## 클래스 나누기
import re
import sys
import random as rd

class VendingMachine :
    
    def __init__(self):
    
        # 자판기 음료 종류
        self.a_menu_dict = {
            'coffee' : 500
            ,'coke' : 1000
            ,'fanta' : 1000
            ,'cider' : 700
        
        }
        
        # 재고 확인 리스트
        self.a_menu_cnt_dict = {
            'coffee' : rd.randrange(1,11)
            ,'coke' : rd.randrange(1,11)
            ,'fanta' : rd.randrange(1,11)
            ,'cider' : rd.randrange(1,11)
        }
        
        self.i_coin = 0

    # 반환 여부
    ## 돈 받을지 여부 확인 
    def choice(self):
        s_choice = input('반환할거니? (y/n): ')
        a_choice = ['y','n']
        b_choice = False
        if s_choice.lower().strip() in a_choice:
            if s_choice.lower().strip() == 'n':
                b_choice = False
            else:
                b_choice = True
        else:
            print('재질문 합니다.')
            self.choice()
        return b_choice


    # 입금
    def insert(self, i_coin = 0 ) :
        s_input = input('금액을 넣어주세요 : ')
        
        if re.match('[0-9]{2,4}$', s_input) : 
            i_input = s_input.strip()
            if (int(i_input) % 10) == 0 :
                i_coin = int(i_input) + i_coin
                self.i_coin = i_coin
                print('총 %d원 입금하셨습니다. ' %self.i_coin)
                
            else : 
                print('이렇게 넣으면 안돼여!!')
                self.insert(i_coin)
        else :
            print('이렇게 넣으면 안돼여!!')
            self.insert(i_coin)

        return i_coin
    
    
    # 메뉴 선택
    def select(self, i_coin) :    
        
        for s_menu_type, i_menu_cnt in self.a_menu_cnt_dict.items() :
            s_menu = '%s : %d개'%(s_menu_type, i_menu_cnt)
            print(s_menu, end = '\t')
                    
        s_choice = input('\n음료를 선택해주세요 : ')
        if re.match('[a-zA-Z]{1,6}$', s_choice.strip()) :
            s_choice_item = s_choice.lower().strip()
                    
            if self.a_menu_cnt_dict.get(s_choice_item) > 0 :
                self.a_menu_cnt_dict[s_choice_item] -= 1
                i_money = i_coin - self.a_menu_dict.get(s_choice_item)
                print("%s 음료가 나왔습니다." %s_choice_item)
                if i_money > 500 :
                    self.calc_change(i_money) 
                    self.more(i_money)
                else :
                    self.check(i_money)
                
            else :
                print('재고 없으니 다른 상품을 골라주세요. ')
                self.select(i_coin)
            
        # 잘못입력
        else :
            print('다시 입력해주세요. ')
            self.select(i_coin)
        
        return i_money             

    # 더 살건지???
    def more(self, i_money) :
        s_another = input('더 살래? [y/n]\n')
        a_another = ['y','n']
        
        if s_another.lower().strip() in a_another :
            if s_another.lower().strip() == 'n':
                print('그럼 반환할게')
                self.calc_change(i_money)
            else:
                self.select(i_money)
        else :
            print('다시 입력해주세요. ')
            self.check(i_money)
    
    # 잔돈 구하기 
    def calc_change(self, i_money) :

        # 잔돈
        a_money_dict = { 
            1000 : 0
            ,500 : 0
            ,100 : 0
            ,50 : 0
            ,10 : 0
        }
        
        # i_money_ori = i_money

        # 계산      
        a_money_dict[1000] = i_money // 1000
        i_money = i_money % 1000
        a_money_dict[500] = i_money // 500
        i_money = i_money % 500
        a_money_dict[100] = i_money // 100
        i_money = i_money % 100
        a_money_dict[50] = i_money // 50
        i_money = i_money % 50
        a_money_dict[10] = i_money // 10
        
        for i_cnt in a_money_dict.keys() :
            if a_money_dict[i_cnt] < 0 :
                a_money_dict[i_cnt] = 0
        
        
        for i_money_unit, i_money_cnt in a_money_dict.items() :
            s_money = '%d원 : %d개'%(i_money_unit, i_money_cnt)
            print(s_money)
        
    
    # 디스플레이
    def display(self) :
        print("#"*100)
        print("넷크루즈 자판기")
        print("-"*100)
        
        for s_menu, i_menu_price in self.a_menu_dict.items():
            print("%s : %d" %(s_menu, i_menu_price), end='\t')
        
        print()
        
        for s_menu, i_menu_rest in self.a_menu_cnt_dict.items():
            print("%s : %d" %(s_menu, i_menu_rest), end='\t')
        
        print()
        print("#"*100)


    # 돈을 더 넣을 것인지?
    def check(self, i_money) :
        s_another = input('\n돈 더 넣을래?[y/n]')
        a_another = ['y','n']
        
        if s_another.lower().strip() in a_another :
            if s_another.lower().strip() == 'n':
                self.calc_change(i_money)
            else:
                self.insert(i_money)
        else :
            print('다시 입력해주세요. ')
            self.check(i_money)

    #시작
    def main(self):
        self.display()
        
        #시작부입니다. 

        i_coin = self.insert()
        self.select(i_coin)
        
            
if __name__ == '__main__':
    o_vm = VendingMachine()
    
    try:
        o_vm.main()
    except Exception as e:
        print('자판기 부팅이 안됩니다. ')
        print(str(e))
    
