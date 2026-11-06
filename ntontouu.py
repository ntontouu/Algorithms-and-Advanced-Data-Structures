import hashlib
import math
import random
import string
import time
import sys
import matplotlib.pyplot as plt
import numpy as np

class BloomFilter:
    def __init__(self, m, k):
        self.m = m  #ΜΕΓΕΘΟΣ ΠΙΝΑΚΑ ΠΟΣΑ BITS ΘΑ ΕΧΩ
        self.k = k  #ΠΟΣΕΣ ΦΟΡΕΣ ΘΑ ΤΡΕΞΕΙ Η ΧΑΣ
        self.bit_array = [0] * self.m

    def _hash_functions(self, item):
        #ФTIAXΝΩ K ΔΕΙΚΤΕΣ ΜΕ Χ2 ΧΑΣ ΓΙΑ ΝΑ ΜΗΝ ΓΡΑΦΩ 100 ΣΥΝΑΡΤΗΣΕΙΣ
        #ΚΟΒΩ ΤΟ MD5 ΣΤΗ ΜΕΣΗ ΚΑΙ ΠΑΙΡΝΩ 2 ΚΟΜΜΑΤΙΑ
        hash_md5 = hashlib.md5(item.encode('utf-8')).hexdigest()
        h1 = int(hash_md5[:16], 16)
        h2 = int(hash_md5[16:], 16)
        
        indices = []
        for i in range(self.k):
            #ΤΥΠΟΣ ΓΙΑ ΝΑ ΒΓΟΥΝ ΤΑ INDEXΕΣ 
            idx = (h1 + i * h2) % self.m
            indices.append(idx)
        return indices

    def insert(self, item):
        #ΜΠΑΙΝΕΙ ΣΤΟΝ ΠΙΝΑΚΑ ΚΑΝΟΝΤΑΣ ΤΑ BITS ΑΣΣΟΥΣ
        indices = self._hash_functions(item)
        for idx in indices:
            self.bit_array[idx] = 1

    def query(self, item):
        #ΨΑΧΝΩ ΑΝ ΕΙΝΑΙ ΜΕΣΑ
        indices = self._hash_functions(item)
        for idx in indices:
            if self.bit_array[idx] == 0:
                #ΑΝ ΕΣΤΩ ΚΑΙ ΕΝΑ ΕΙΝΑΙ 0  ΔΕΝ ΕΙΝΑΙ ΜΕΣΑ
                return False
        #ΑΝ ΕΙΝΑΙ ΟΛΑ 1 ΜΑΛΛΟΝ ΕΙΝΑΙ ΜΕΣΑ FALSE POSITIVE ΠΑΙΖΕΙ
        return True


class CountingBloomFilter:
    def __init__(self, m, k):
        self.m = m
        self.k = k
        self.counters = [0] * self.m

    def _hash_functions(self, item):
        #ΙΔΙΑ ΔΟΥΛΕΙΑ ΜΕ ΤΟ ΑΠΟ ΠΑΝΩ ΚΟΒΩ ΤΟ MD5
        hash_md5 = hashlib.md5(item.encode('utf-8')).hexdigest()
        h1 = int(hash_md5[:16], 16)
        h2 = int(hash_md5[16:], 16)
        
        indices = []
        for i in range(self.k):
            idx = (h1 + i * h2) % self.m
            indices.append(idx)
        return indices

    def insert(self, item):
        indices = self._hash_functions(item)
        for idx in indices:
            #ΠΑΕΙ ΜΕΧΡΙ 15 ΓΙΑΤΙ ΤΟΣΟ ΧΩΡΑΕΙ ΕΝΑ 4-ΜΠΙΤ. ΑΝ ΠΑΕΙ ΠΑΡΑΠΑΝΩ ΜΕΝΕΙ ΕΚΕΙ
            if self.counters[idx] < 15:
                self.counters[idx] += 1

    def query(self, item):
        #ΑΝ ΚΑΠΟΙΟΣ ΜΕΤΡΗΤΗΣ ΕΙΝΑΙ 0 ΤΟΤΕ ΤΟ ΣΤΟΙΧΕΙΟ ΑΓΝΟΕΙΤΑΙ
        indices = self._hash_functions(item)
        for idx in indices:
            if self.counters[idx] == 0:
                return False
        return True

    def delete(self, item):
        #ΔΙΑΓΡΑΦΗ ΜΟΝΟ ΑΝ ΤΟ ΕΙΝΑΙ ΜΕΣΑ
        if self.query(item) == True:
            indices = self._hash_functions(item)
            for idx in indices:
                if self.counters[idx] > 0:
                    self.counters[idx] -= 1


def get_random_string(length=8):
    #ΦΤΙΑΧΝΕΙ ΤΥΧΑΙΑ ΣΤΡΙΝΓΚ ΓΙΑ ΤΑ ΤΕΣΤ
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

#ΟΠΤΙΚΟΠΟΙΗΣΗ
def visualize_results(m_sizes, fp_percentages, times, memories):
    # Φτιάχνουμε ένα παράθυρο με 3 γραφήματα στη σειρά (1 γραμμή, 3 στήλες)
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('Αξιολόγηση Απόδοσης Counting Bloom Filter', fontsize=16, fontweight='bold')

    #ΓΡΑΒΔΟΓΡΑΜΜΑ ΓΙΑ ΨΕΥΔΗ ΘΕΤΙΚΑ
    bars = axs[0].bar([str(m) for m in m_sizes], fp_percentages, color=['#e74c3c', '#f39c12', '#2ecc71'])
    axs[0].set_title('Ποσοστό False Positives (%)')
    axs[0].set_xlabel('Μέγεθος Πίνακα (m)')
    axs[0].set_ylabel('Λανθασμένα Θετικά (%)')
    # Βάζουμε τα νουμεράκια πάνω από κάθε μπάρα
    for bar in bars:
        yval = bar.get_height()
        axs[0].text(bar.get_x() + bar.get_width()/2, yval + 0.1, f'{yval:.1f}%', ha='center', va='bottom')

    #ΓΡΑΦΙΜΑ ΣΥΓΚΡΙΣΗΣ ΧΡΟΝΩΝ
    labels = ['Εισαγωγή (10k)', 'Αναζήτηση (1k)']
    bf_times = [times['bf_insert'], times['bf_query']]
    set_times = [times['set_insert'], times['set_query']]
    
    x = np.arange(len(labels))
    width = 0.35  
    axs[1].bar(x - width/2, bf_times, width, label='Bloom Filter', color='#3498db')
    axs[1].bar(x + width/2, set_times, width, label='Python Set', color='#95a5a6')
    
    axs[1].set_title('Χρόνος Εκτέλεσης (Δευτερόλεπτα)')
    axs[1].set_xticks(x)
    axs[1].set_xticklabels(labels)
    axs[1].legend()

    #ΠΙΤΑ ΜΝΗΜΗΣ
    axs[2].pie([memories['bf'], memories['set']], 
               labels=[f"Bloom Filter\n({memories['bf']} B)", f"Python Set\n({memories['set']} B)"], 
               autopct='%1.1f%%', 
               startangle=140, 
               colors=['#2ecc71', '#e74c3c'],
               explode=(0.1, 0)) # Το explode "πετάει" λίγο έξω το κομμάτι του Bloom Filter για έμφαση
    axs[2].set_title('Κατανάλωση Μνήμης')

    #ΠΙΟ ΟΜΟΡΦΟ ΚΑΙ ΕΜΦΑΝΙΣΗ
    plt.tight_layout()
    plt.show()


def main():
    print("--- 1. ΕΛΕΓΧΟΣ ΟΡΘΟΤΗΤΑΣ (ΜΕΤΡΗΤΕΣ & ΔΙΑΓΡΑΦΗ) ---")
    cbf = CountingBloomFilter(m=1000, k=3)
    
    #3 ΦΡΟΥΤΑ
    for word in ["apple", "banana", "cherry"]:
        cbf.insert(word)
        
    print("ΥΠΑΡΧΕΙ ΤΟ 'apple' ΠΡΙΝ ΤΟ ΔΙΑΓΡΑΨΟΥΜΕ? :", cbf.query("apple"))
    
    cbf.delete("apple")
    print("ΥΠΑΡΧΕΙ ΤΟ 'apple' ΑΦΟΥ ΤΟ ΣΒΗΣΑΜΕ?    :", cbf.query("apple"))
    print("ΤΟ 'banana' ΕΠΗΡΕΑΣΤΗΚΕ ΑΠΟ ΤΟ ΣΒΗΣΙΜΟ? :", cbf.query("banana"))
    print()

    print("--- 2. ΠΕΙΡΑΜΑΤΑ ΜΕ ΤΑ FALSE POSITIVES ---")
    n_elements = 10000
    n_tests = 1000
    
    #10Κ ΛΕΞΕΙΣ
    inserted_data = [get_random_string() for _ in range(n_elements)]
    
    #1Κ ΛΕΞΕΙΣ ΝΕΕΣ ΓΙΑ ΕΛΕΓΧΟ
    test_data = []
    while len(test_data) < n_tests:
        candidate = get_random_string()
        if candidate not in inserted_data:
            test_data.append(candidate)
            
    #ΤΑ 3 ΜΕΓΕΘΗ ΓΙΑ ΤΟΝ ΠΙΝΑΚΑ
    m_sizes = [50000, 100000, 200000]
    fp_results_for_plot = []

    for m in m_sizes:
        #ΥΠΟΛΟΓΙΣΜΟΣ Κ
        #ΑΝ ΒΓΕΙ 0 ΤΟ ΚΑΝΩ 1 ΓΙΑΤΙ ΑΛΛΙΩΣ ΘΑ ΣΚΑΣΕΙ
        optimal_k = int((m / n_elements) * math.log(2))
        if optimal_k == 0: 
            optimal_k = 1  
            
        bf = BloomFilter(m, optimal_k)
        
        #ΓΕΜΙΖΩ ΤΟ ΦΙΛΤΡΟ
        for item in inserted_data:
            bf.insert(item)
            
        #ΜΕΤΡΑΩ ΠΟΣΕΣ ΦΟΡΕΣ ΕΔΩΣΕ FALSE POSITIVE 
        false_positives = 0
        for item in test_data:
            if bf.query(item) == True:
                false_positives += 1
                
        fp_percentage = (false_positives / n_tests) * 100
        fp_results_for_plot.append(fp_percentage)
        print(f"ΓΙΑ m={m} ΚΑΙ k={optimal_k} ΕΚΑΝΕ ΛΑΘΟΣ: {false_positives}/{n_tests} ({fp_percentage}%)")

    print("\n--- 3. ΣΥΓΚΡΙΣΗ ΜΕ ΤΟ SET ΤΗΣ PYTHON ---")
    m_compare = 100000
    k_compare = int((m_compare / n_elements) * math.log(2))
    
    bf_comp = BloomFilter(m_compare, k_compare)
    python_set = set()

    #ΠΟΣΗ ΩΡΑ ΠΑΙΡΝΕΙ ΝΑ ΓΕΜΙΣΕΙ ΤΟ BLOOM FILTER
    start = time.time()
    for item in inserted_data:
        bf_comp.insert(item)
    bf_time_insert = time.time() - start

    #ΠΟΣΗ ΩΡΑ ΠΑΙΡΝΕΙ ΝΑ ΓΕΜΙΣΕΙ ΤΟ PYTHON SET
    start = time.time()
    for item in inserted_data:
        python_set.add(item)
    set_time_insert = time.time() - start

    #ΠΟΣΗ ΩΡΑ ΠΑΙΡΝΕΙ Η ΑΝΑΖΗΤΗΣΗ ΣΤΟ BLOOM FILTER
    start = time.time()
    for item in test_data:
        bf_comp.query(item)
    bf_time_query = time.time() - start

    #ΠΟΣΗ ΩΡΑ ΠΑΙΡΝΕΙ Η ΑΝΑΖΗΤΗΣΗ ΣΤΟ PYTHON SET
    start = time.time()
    for item in test_data:
        _ = item in python_set
    set_time_query = time.time() - start

    #ΥΠΟΛΟΓΙΖΩ ΣΤΟ ΠΕΡΙΠΟΥ ΤΟ BLOOM ΚΑΙ ΜΕ ΤΗΝ PYTHON ΤΟ SET
    bf_memory_bytes = m_compare // 8
    set_memory_bytes = sys.getsizeof(python_set) + sum(sys.getsizeof(i) for i in python_set)

    print(f"ΧΡΟΝΟΣ ΕΙΣΑΓΩΓΗΣ : BloomFilter = {bf_time_insert:.4f}s | Set = {set_time_insert:.4f}s")
    print(f"ΧΡΟΝΟΣ ΑΝΑΖΗΤΗΣΗΣ: BloomFilter = {bf_time_query:.4f}s | Set = {set_time_query:.4f}s")
    print(f"ΠΟΣΗ ΜΝΗΜΗ ΤΡΩΕΙ : BloomFilter = {bf_memory_bytes} bytes | Set = {set_memory_bytes} bytes")

    times_dict = {
            'bf_insert': bf_time_insert,
            'set_insert': set_time_insert,
            'bf_query': bf_time_query,
            'set_query': set_time_query
        }
    mem_dict = {
            'bf': bf_memory_bytes,
            'set': set_memory_bytes
        }
    visualize_results(m_sizes, fp_results_for_plot, times_dict, mem_dict)

if __name__ == "__main__":
    main()