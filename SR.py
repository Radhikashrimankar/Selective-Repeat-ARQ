import random
import pickle
import time

#-------------------------------------------------------------------------------------------------------
tot_frames = 16
n = 3
m = pow(2,n)
frame_send_at_instance = (m // 2)
send = []
rcvd = []
rcvd_ack = []
t = 0
arr = []
duplicate = []
rw = frame_send_at_instance
sw = frame_send_at_instance
file = ''
file = open("the.txt","ab")
file.seek(0)
file.truncate(0)
packet = []
flow = []
packet1 = []
size = 0

for i in range(tot_frames) :
    arr.append(t)
    t = (t+1)%m

for i in range(frame_send_at_instance) :
    send.append(arr[i])
    rcvd.append(arr[i])
    rcvd_ack.append('n')

#-------------------------------------------------------------------------------------------------------

def receiver() :
    global m
    global frame_send_at_instance
    global rcvd_ack
    global send
    global rcvd,flow,tot_frames
    global rw
    global arr
    global sw,duplicate
    global packet,file,packet1,size
    
    while size < tot_frames :
        for i in range(frame_send_at_instance) :
            if rcvd_ack[i] == 'n' :
                f = random.randint(0,9)
                if f != 5 :
                    j = 0
                    
                    while j < frame_send_at_instance :
                        if rcvd[j] == send[i] :
                            print("RECEIVER SIDE : Frame ",rcvd[j]," received correctly")
                            rcvd[j] = arr[rw]
                            rw = (rw+1) % m
                            break
                        j += 1
                    a1 = random.randint(0,4)
                    print("--------------------------------------------------------------------------------")
                    if a1  == 3 :
                        print("RECEIVER SIDE : Acknowledgement : ",send[i]," lost)")
                        packet.append(["Acknowledgement Lost",send[i]])
                        rcvd_ack[i] = 'n'
                        flow.append(1)
                        size += 1
                        print("--------------------------------------------------------------------------------")
                    else :
                        print("SENDER SIDE   : Acknowledgement ",send[i]," received ")
                        packet.append(["Acknowledgement Received",send[i]])
                        rcvd_ack[i] = 'p'
                        flow.append(2)
                        size += 1
                        print("--------------------------------------------------------------------------------")
                else :
                    ld = random.randint(0,1)
                    if ld == 0:
                        print("RECEIVER SIDE : Frame ",send[i]," is damaged.")
                        packet.append(["Frame Damaged",send[i]])
                        print("RECEIVER SIDE : Negative Acknowledgement ",send[i]," send")
                        flow.append(3)
                        print("--------------------------------------------------------------------------------")
                    else :
                        print("SENDER SIDE   : Frame ",send[i]," is lost")
                        packet.append(["Frame Lost",send[i]])
                        print(" Sender Timeouts -- Resend Frame")
                        flow.append(4)
                        print("--------------------------------------------------------------------------------")
        
        b = 0

        while b < frame_send_at_instance :
            if (rcvd_ack[b] == 'n' and flow[b] == 4) or (rcvd_ack[b] == 'n' and flow[b] == 3) :
                break
            b += 1
            
        i = 0

        
        for k in range(b,frame_send_at_instance) :
            
            if rcvd_ack[k] == 'n' and ( flow[k] != 1 and flow[k] != 2 ):
                rcvd_ack[i] = 'n'
                send[i] = send[k]
                packet1.append('yes')
                i+= 1

        flow = []        
        if len(packet1) > 0 :
            frame_send_at_instance = len(packet1)
            packet1 = []
        else :
            frame_send_at_instance = 4
            if i != frame_send_at_instance :
                for k in range(i,frame_send_at_instance) :
                    send[k] = arr[sw]
                    sw = (sw + 1)%m
                    rcvd_ack[k] = 'n'
        
        pickle.dump(packet,file)
        print("--------------------------------------------------------------------------------")
        ch = input('Do You want to transfer again : ')
        print("--------------------------------------------------------------------------------")
        if ch == 'y' and size < tot_frames:
            sender()
        else :
            print('All frames send')
            exit()


#-------------------------------------------------------------------------------------------------------

def sender() :
    global m
    global frame_send_at_instance
    global rcvd_ack
    global send
    global duplicate
    global packet,file,packet1,size,tot_frames

    if size >= tot_frames :
        print('All frames send')
        time.sleep(5)
        exit()
    elif tot_frames - size < 4 :
        frame_send_at_instance = tot_frames - size

    packet = []
    
    print("--------------------------------------------------------------------------------")
    for i in range(frame_send_at_instance) :
        print("SENDER : Frame : ",send[i]," is sent")
        packet.append(send[i])
    print("--------------------------------------------------------------------------------")
   
    receiver()

sender()
#-------------------------------------------------------------------------------------------------------
