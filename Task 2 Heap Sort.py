def heapify(arr, n, i):
    largest = i #set the largest index to be i
    left = 2 * i + 1  #set 'left' to be the left hand index
    right = 2 * i + 2 #set 'right' to be the right hand index

    if left < n and arr[left] > arr[largest]: #compare left index with the largest 
        largest = left #if left index is larger than the largest left index equal to largest

    if right < n and arr[right] > arr[largest]: #compare tight index with the largest 
        largest = right #if right index is larger than the largest right index equal to largest

    if largest != i: #if the largest index does not equal to the original largest index
        arr[i], arr[largest] = arr[largest], arr[i] #largest index switch with the last index
        heapify(arr, n, largest)

def heapSort(arr):
    n = len(arr) 

    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)

if __name__ == "__main__":
    arr = list(map(int, input("Enter space-separated number: ").split())) #Let user input an array by typing space-separated number
    print(arr)
    heapSort(arr)
    print(arr)
    