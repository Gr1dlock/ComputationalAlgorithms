import process
import input_data

if __name__ == '__main__':
    # data = input_data.get_data()
    # p = process.find_p(data)
    t = int(input("T: "))
    p = int(input("P: "))
    nt = process.count_nt(t, p)
    # print("p = ", p)
