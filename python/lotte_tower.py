# 1 ~ 100층까지 표시
# 현재 층수 표시
# 문은 2초 후에 열림

# 1 ~ 20 => 아무나 출입 가능
# 21 ~ 40 => 회사 업무 공간이므로 승인된 사람만
#               - 승인방법) 해당 층수 + @2@ + 오늘날짜(11월 11일 - 1111)
#               - 예제) 24@2@1115

# 41층~60층 - 상업적 공간으로 비용을 지불한 사람만 이용 가능 
#               - 출입시 비용은 카드 또는 현금 지불을 한다
#               - 현금/카드 비용(상동) : 5만원
#               - 카드 번호 형식은 13자리(***-****-*****)

# 61층~100층 - private 한 주거구역 승인된 사람만 이용가능
#               승인방법) http://... 에 기재된 사이트 접속후 승인 요청후 발급되는 key를 Decryption 후 해당 층의 비밀번호 등록후 이용
#               주의) 61층 ~ 69층  - 열쇠 필요
#                     71층 ~ 79층  - 지문도어락 필요
#                     81층 ~ 89층  - 프론트키 필요
#                     91층 ~ 100층 - 마스터키 필요 
#               총 4개의 구역은 각기 다른 암호화 방식 채택

import re
import sys
import time
import datetime
import requests
import base64
import string
import hashlib
from Crypto.Util.Padding import unpad
from Crypto.Cipher import AES


class LotteTower :
    def __init__(self) :
        self.i_cash = 0
        
        self.s_url = 'http://10.50.1.53/index.php'
        
    # 층수 입력
    def input_floor(self) :
        while True :
            s_btn = input('층수를 입력해주세요 : ')
            
            if re.match('^[0-9]{1,3}$',s_btn.strip()) :
                i_floor = int(s_btn.strip())

                if i_floor <= 0 :
                    print('해당 층은 존재하지 않으니 다시 입력해주세요. ')
                elif i_floor > 100 :
                    print('해당 층은 존재하지 않으니 다시 입력해주세요. ')
                else :
                    self.select_floor(i_floor)
                    break
            else : 
                print('다시 입력해주세요. ')
            
    
    # 구역별로 나눠서 보내줌
    def select_floor(self, i_floor ) :
        
        if i_floor < 21 :
            ## 일반층 호출
            self.elevator(i_floor)
        elif i_floor > 20 and i_floor < 41 :
            ## 업무층 호출
            self.work_access(i_floor)
        elif i_floor > 40 and i_floor < 61 :
            ## 상업층 호출
            self.payment(i_floor)
            
        # 주거층
        elif i_floor > 60 and i_floor < 71 :
            ## 열쇠 필요
            s_password = self.get_key(i_floor)
            b_approve = self.resi_60(s_password, i_floor)
            self.isApprove(b_approve, i_floor)
            
        elif i_floor > 70 and i_floor < 81 :
            ## 지문도어락 필요
            s_password = self.get_key(i_floor)
            b_approve = self.resi_70(s_password, i_floor)
            self.isApprove(b_approve, i_floor)
            
        elif i_floor > 80 and i_floor < 91 :
            ## 프론트키 필요
            s_password = self.get_key(i_floor)
            b_approve = self.resi_80(s_password, i_floor)
            self.isApprove(b_approve, i_floor)

        elif i_floor > 90 and i_floor < 100 :
            ## 마스터키 필요
            s_password = self.get_key(i_floor)
            b_approve = self.resi_90(s_password, i_floor)
            self.isApprove(b_approve, i_floor)
        else  :
            ## 100층
            s_password = self.get_key(i_floor)
            b_approve = self.resi_100(s_password, i_floor)
            self.isApprove(b_approve, i_floor)
    
    
    # 엘리베이터 가동
    def elevator(self, i_floor) :
        time.sleep(1)
        print('%d층을 선택하셨습니다. ' %i_floor)
        print('올라갑니다. ')
        time.sleep(2)
        print('엘리베이터 동작 시작')
        
        print('='*100)
        print('1 2 3 4 5 6 7 8 9 10 ... 95 96 97 98 99 100')
        for i_idx in range(1, i_floor + 1) :
            print('#', end = ' ' )
            time.sleep(0.25)
            sys.stdout.flush()
        time.sleep(0.25)
        print('[%d층]' %i_floor)
        
        print('=' * 100 + '\n')
        time.sleep(2)
        print('문이 열립니다. ')
        time.sleep(1)
    
    
    # 돈 받음(카드 또는 현금) - 상가
    def payment(self,i_floor) :
        print('결제가 필요한 구역입니다. (5만원)\n')
        s_input_pay = input('[카드] | [현금] : ')
        s_payment = s_input_pay.strip().replace(' ', '')
        
        if (s_payment == '카드') :
            self.payment_card(i_floor)

        elif (s_payment == '현금') : 
            self.payment_cash(i_floor)
        else :
            # 뭔가의 이상한 입력
            b_answer = self.cancel()
            if b_answer is True :
                print('다시 입력해주세요.')
                self.payment(i_floor)
    
    
    # 현금결제
    def payment_cash(self, i_floor, i_cash = 0) :
        s_cash = input('현금을 넣어주세요 : ')
            
        if re.match('^[0-9]{1,5}', s_cash) :
            s_cash = s_cash.strip()
            i_cash = int(s_cash)
            self.i_cash += i_cash
                
            # 처음부터 5만원을 넘게 준 경우 => 남은 돈 뱉어내기
            if self.i_cash > 50000 :
                i_rtn = abs(50000 - self.i_cash)
                print('결제 완료 : %d원이 반환됩니다. ' %i_rtn)
                self.elevator(i_floor)

            # 조금씩 주는 경우
            elif self.i_cash < 50000 : 
                i_rtn = abs(50000 - self.i_cash)
                print('결제 완료까지 남은 금액 : %d' %i_rtn) 
                self.payment_cash(i_floor, self.i_cash)

            # 금액 5만원에 맞춰서 준 경우 => 결제 완료 띄우고 올려보내기
            elif self.i_cash == 50000 :
                print('결제 완료')
                self.elevator(i_floor)
            else :
                pass  
        else :
            print('입력 오류')
            self.payment_cash(i_floor)
    
    
    # 카드 결제
    def payment_card(self, i_floor) :
        s_card = input('카드 번호를 입력해주세요 (13자리 ): ')
        s_card_num = s_card.replace('-', '')
        s_card_num = re.findall('\d', s_card_num)
        
        if len(s_card_num) == 13 :
            print('5만원이 결제되었습니다. ')
            self.elevator(i_floor)
        else : 
            b_answer = self.cancel()
            if b_answer is True :
                print('다시 입력해주세요.')
                self.payment_card(i_floor)
            

    # 승인번호 - 업무
    def work_access(self, i_floor) :
        s_today = datetime.date.today()
        s_password = str(i_floor) + '@2@' + s_today.strftime('%m%d')
        
        s_input_pw = input('승인 암호를 입력해주세요 : ')
        
        if s_input_pw.replace(' ','') == s_password :
            print('승인 되었습니다. ')
            ## 엘리베이터 가동(문열림)
            self.elevator(i_floor)
        else : 
            print('암호가 일치하지 않습니다. ')
            # 암호 재입력 또는 층수 변경
            b_answer = self.cancel()
            if b_answer is True :
                self.work_access(i_floor)

    
    # 암호 가져옴
    def get_key(self, i_floor) :
        
                
        a_params_dict = {
            'flow' : i_floor
            ,'api' : 1
        }
        
        s_request = requests.get(self.s_url, params = a_params_dict)
        
        a_key_dict = s_request.json()
        s_password = a_key_dict.get('password')
        
        return s_password
    
    ## 61층 ~ 70층
    def resi_60 (self, s_password, i_floor) :
        # 그냥 password 받아서 복호화 시키면 됨
        s_key = s_password
        s_decoding = base64.b64decode(s_key)
        s_access_key = s_decoding.decode('ascii')
        
        a_params_dict = {
            'flow' : i_floor
            ,'password' : s_access_key[3:]
        }
        s_request = requests.post(self.s_url, data = a_params_dict)
        
        a_access_dict = s_request.json()
        b_approve = a_access_dict.get('result')
        
        print('비밀 번호는 ' + a_params_dict.get('password'))
        
        return b_approve
    
    ## 71층 ~ 80층
    def resi_70 (self, s_password, i_floor) :
        # password 받으면 문자열 뒤집어서 복호화
        s_key = s_password[::-1]
        s_decoding = base64.b64decode(s_key)
        s_access_key = s_decoding.decode('ascii')
        
        a_params_dict = {
            'flow' : i_floor
            ,'password' : s_access_key[3:]
        }
        
        s_request = requests.post(self.s_url, data = a_params_dict)
        
        a_access_dict = s_request.json()
        b_approve = a_access_dict.get('result')
        
        print('비밀 번호는 '+ a_params_dict.get('password'))
        
        return b_approve
    
       
    ## 81층 ~ 90층
    def resi_80 (self, s_password, i_floor) :
        # password 받으면 특문 제거 후 문자열 뒤집어서 복호화
        s_key = s_password[::-1]
        s_key_clr = ''.join(filter(str.isalnum, s_key))
        s_key_padding = s_key_clr + '='
        
        s_decoding = base64.b64decode(s_key_padding)
        s_access_key = s_decoding.decode('ascii')
        
        a_params_dict = {
            'flow' : i_floor
            ,'password' : s_access_key[3:]
        }
        
        s_request = requests.post(self.s_url, data = a_params_dict)
        
        a_access_dict = s_request.json()
        b_approve = a_access_dict.get('result')
        
        print('비밀 번호는 '+ a_params_dict.get('password'))
        
        return b_approve
    
    ## 91층 ~ 99층
    def resi_90 (self, s_password, i_floor) :
        # key = a~z (2글자)
        a_letter_list = string.ascii_lowercase
        
        for i in range(len(a_letter_list)) :
            for j in range(len(a_letter_list)) :
                s_key_letter = a_letter_list[i]+a_letter_list[j]
                
                try :
                    s_key = hashlib.sha256(s_key_letter.encode()).digest()
                    s_enc = base64.b64decode(s_password)
                    
                    iv = bytes(16)
                    
                    s_de_cipher = AES.new(s_key, AES.MODE_CBC, iv)
                    s_pw = s_de_cipher.decrypt(s_enc)
                
                    s_decrypted = bytes.decode(unpad(s_pw,AES.block_size))
                    
                    a_params_dict = {
                        'flow' : i_floor
                        ,'password' : s_decrypted[::-1]
                    }
                    
                    s_request = requests.post(self.s_url, data = a_params_dict)
                    
                    a_access_dict = s_request.json()
                    print('비밀 번호는 '+ a_params_dict.get('password'))
                    b_approve = a_access_dict.get('result')

                    if b_approve is True :
                        return b_approve   
                    else : 
                        pass
                    
                except Exception as e :
                    s_decrypted = ''
    
    
    ## 100
    def resi_100(self, s_password, i_floor) :
        s_key = s_password.split(' ')
        s_decoding_key = ''
        
        for i_idx in s_key :
            i_bin = int(i_idx, base = 2)
            s_char = chr(i_bin)
            s_decoding_key += s_char
        
        s_decoding = base64.b64decode(s_decoding_key)
        s_access_key = s_decoding.decode('ascii')
        
        a_params_dict = {
            'flow' : i_floor
            ,'password' : s_access_key[4:]
        }
        s_request = requests.post(self.s_url, data = a_params_dict)
        
        a_access_dict = s_request.json()
        b_approve = a_access_dict.get('result')
        
        print('비밀 번호는 '+ a_params_dict.get('password'))

        return b_approve
    
    
    # 주거층 승인 여부
    def isApprove(self, b_approve, i_floor) :
        # True면 인포 띄우고 엘리베이터 가동시키기
        if b_approve is True :
            print('승인되었습니다. ')
            self.elevator(i_floor)
        else : 
            print('승인이 거부되었습니다. ')
            
            
    # 다른 층 고르기
    def cancel(self) :
        while True :
            s_answer = input('다른 층을 고르시겠습니까? [y/n]')
            s_answer = s_answer.lower().strip()
            a_answer_list = ['y','n']   # y가 다른 층 n이 그밖의 선택지
            b_answer = False
                        
            if re.match('[a-z]{1}', s_answer) :
                if s_answer in a_answer_list :
                    if s_answer == 'y' :
                        self.input_floor()
                        break
                    else : 
                        b_answer = True
                        break
                else :
                    print('다시 입력해주세요 . ')      
            
            else :
                print('다시 입력해주세요 . ')
        return b_answer
    
      
    # 메인
    def main(self) :
        print('='*100)
        print('1 2 3 4 5 6 7 8 9 10 ... 90 91 92 93 94 95 96 97 98 99 100')
        print('='*100)
        self.input_floor()


if __name__ == '__main__' :
    o_lt = LotteTower()
    
    try :
        o_lt.main()
        
    except Exception as e :
        print(e)
        print('엘리베이터 가동 중지')

 