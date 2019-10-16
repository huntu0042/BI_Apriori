
def createC1(dataSet):
  C1=[]
  for transaction in dataSet:
    for item in transaction:
      if not [item] in C1:
        C1.append([item])

  C1.sort()
  return map(frozenset, C1)

C1 = createC1(dataset)

D = map(set,dataset) # distinct 수를 뽑아냄. (1,3,3) 이면 (1,3)


# 전체 그룹중에 Ck 가 있는것.
# Ck 가 1 이라면 1을 포함한 그룹들을 찾음 (지지도 생성)
# Ck 가 [1,3] 이라면 [1,3] 둘다 포함한 그룹들의 지지도 찾음

def scanD(D, Ck, minSupport):
    # 요소 n 은 몇개의 그룹에 포함되어 있는지 계산한다. (1은 2개) ssCnt = {}
    for tid in D:  # tid 에는 set([1,3,4]) 등이 담긴다.
        for can in Ck:  # can 에는 frozenset([1]) 등이 담긴다.
            if can.issubset(tid):  # 1 이 [1,3,4] 에 있으면
                if not ssCnt.has_key(can):
                    ssCnt[can] = 1
                else:
                    ssCnt[can] += 1  # 키 : 1 값 : 1을 가진 그룹의 수

    # 지지도가 0.5보다 높은것들의 리스트를 구함.
    # 1의 경우 2군데 포함되었으니 2/4 = 0.5
    # 2의 경우 3/4 , 3의 경우 3/4 , 4의 경우 1/4, 5의 경우 3/4
    numItems = float(len(D))  # 그룹 갯수
    retList = []
    supportData = {}
    for key, value in ssCnt.iteritems():
        support = value / numItems
        if support >= minSupport:
            retList.insert(0, key)
        supportData[key] = support

    return retList, supportData


# [1,3,2,5] 를 # [1,3] [2,5] [2,3] [3,5] 를
# [2,3,5] 이런식으로 만드는 함수

def aprioriGen(Lk, k):
  retList = []
  lenLk = len(Lk)
  for i in range(lenLk):
    for j in range(i+1, lenLk):
      L1 = list(Lk[i])[:k-2]; L2 = list(Lk[j])[:k-2]
      L1.sort(); L2.sort()
      if L1 == L2:
        retList.append(Lk[i] | Lk[j])

  return retList

# 특정 지지도 이상의 값들의 쌍을 찾음
def apriori(dataset, minSupport = 0.5):
  C1 = createC1(dataset)
  D = map(set, dataset)
  L1 , supportData = scanD(D,C1,minSupport)
  L = [L1]
  k=2
  while (len(L[k-2]) > 0):
    Ck = aprioriGen(L[k-2],k)
    Lk,supK = scanD(D,Ck,minSupport) # 후보그룹을 모두 찾는다.
    supportData.update(supK)
    L.append(Lk) #이게 핵심!특정 지지도 이상의 그룹들만 L에 담는다.즉 가지치기
    k += 1
  return L, supportData

if __name__ == "__main__":
  print "apriori 알고리즘"

  dataset = loadDataSet()

  L, suppData = apriori(dataset)
  print "L:" + str(L)
  print "........................."
  print "suppData:" + str(suppData)
