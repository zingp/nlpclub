import jieba
import synonyms
import random
from random import shuffle
from pprint import pprint
"""
EDA数据增强
现在存在问题：随机交换可能出现标点符号相互交换
"""
random.seed(42)

# 同义词替换
def synonym_replacement(words, n, stopwords):
    """替换一个语句中的n个单词为其同义词"""
    new_words = words.copy()
    random_word_list = list(set([w for w in words if w not in stopwords]))
    random.shuffle(random_word_list)
    num_replaced = 0 
    for word in random_word_list: 
        synonym_words = get_synonyms(word)
        if len(synonym_words) >= 1:
            synonym = random.choice(synonym_words)
            new_words = [synonym if w == word else w for w in new_words]
            num_replaced += 1
        if num_replaced >= n: 
            break
    sentence = ' '.join(new_words)
    new_words = sentence.split(' ')
    return new_words


def get_synonyms(word):
    return synonyms.nearby(word)[0]


# 随机插入
def random_insertion(words, n):
    """随机在语句中插入n个词"""
    new_words = words.copy()
    for _ in range(n):
        add_word(new_words)
    return new_words


def add_word(new_words):
    """从源句子中随机找出十个词的同义词，随机选择一个随机插入到句子中
    """
    synonyms = []
    counter = 0    
    while len(synonyms) < 1:
        random_word = new_words[random.randint(0, len(new_words)-1)]
        synonyms = get_synonyms(random_word)
        counter += 1
        if counter >= 10:
            return
    random_synonym = random.choice(synonyms)
    random_idx = random.randint(0, len(new_words)-1)
    new_words.insert(random_idx, random_synonym)


# 随机交换：Randomly swap two words in the sentence n times
def random_swap(words, n):
    new_words = words.copy()
    for _ in range(n):
        new_words = swap_word(new_words)
    return new_words


def swap_word(new_words):
    idx1 = random.randint(0, len(new_words)-1)
    idx2 = idx1
    counter = 0
    while idx2 == idx1:
        idx2 = random.randint(0, len(new_words)-1)
        counter += 1
        if counter > 3:
            return new_words
    new_words[idx1], new_words[idx2] = new_words[idx2], new_words[idx1]
    return new_words


# 随机删除：以概率p删除语句中的词
def random_deletion(words, p):
    if len(words) == 1:
        return words
    new_words = []
    for word in words:
        r = random.uniform(0, 1)
        if r > p:
            new_words.append(word)
    if len(new_words) == 0:
        rand_int = random.randint(0, len(words)-1)
        return [words[rand_int]]
    return new_words


# EDA函数
def eda(sentence, stopwords, alpha_sr=0.1, alpha_ri=0.1, 
        alpha_rs=0.1, p_rd=0.1, num_aug=9, cha=""):
    seg_list = jieba.cut(sentence)
    seg_list = " ".join(seg_list)
    words = list(seg_list.split())
    num_words = len(words)

    augmented_sentences = []
    num_new_per_technique = int(num_aug/4) + 1
    n_sr = max(1, int(alpha_sr * num_words))
    n_ri = max(1, int(alpha_ri * num_words))
    n_rs = max(1, int(alpha_rs * num_words))

    # 同义词替换sr
    for _ in range(num_new_per_technique):
        a_words = synonym_replacement(words, n_sr, stopwords)
        augmented_sentences.append(cha.join(a_words))

    # 随机插入ri
    for _ in range(num_new_per_technique):
        a_words = random_insertion(words, n_ri)
        augmented_sentences.append(cha.join(a_words))
    
    # 随机交换rs
    for _ in range(num_new_per_technique):
        a_words = random_swap(words, n_rs)
        augmented_sentences.append(cha.join(a_words))

    # 随机删除rd
    for _ in range(num_new_per_technique):
        a_words = random_deletion(words, p_rd)
        augmented_sentences.append(cha.join(a_words))
    
    # print(augmented_sentences)
    shuffle(augmented_sentences)

    if num_aug >= 1:
        augmented_sentences = augmented_sentences[:num_aug]
    else:
        keep_prob = num_aug / len(augmented_sentences)
        augmented_sentences = [s for s in augmented_sentences if random.uniform(0, 1) < keep_prob]

    # augmented_sentences.append(seg_list)
    augmented_sentences.append(sentence)
    return augmented_sentences


def eda_augment(textlist, stopwords, n):
    """
    eda文本增强
    textlist: 文本列表
    n: 生成增强文本数量
    return: 列表，增强的文本
    """
    augment_list = []
    for snetence in textlist:
        eda_list = eda(snetence, stopwords, num_aug=n)
        augment_list.extend(eda_list)
    return augment_list   


if __name__ == "__main__":
    from utils import load_data
    stopwords = load_data("../../data/stopwords.txt")
    sentence = ["明确党在新时代的强军目标是建设一支听党指挥、能打胜仗、作风优良的军队。"]
    ans = eda_augment(sentence, stopwords, 20)
    pprint(ans)
