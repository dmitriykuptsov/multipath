a = [2, 1, 3, 0]
def sort(a):
	for i in range(0, len(a)):
		for j in range(i, len(a)):
			if a[i] > a[j]:
				tmp = a[i]
				a[i] = a[j]
				a[j] = tmp
	return a

print(sort(a))
