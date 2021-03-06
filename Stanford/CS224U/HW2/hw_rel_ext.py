#!/usr/bin/env python
# coding: utf-8

# # Homework and bake-off: Relation extraction using distant supervision

# In[1]:


__author__ = "Bill MacCartney and Christopher Potts"
__version__ = "CS224u, Stanford, Spring 2020"


# ## Contents
# 
# 1. [Overview](#Overview)
# 1. [Set-up](#Set-up)
# 1. [Baselines](#Baselines)
#   1. [Hand-build feature functions](#Hand-build-feature-functions)
#   1. [Distributed representations](#Distributed-representations)
# 1. [Homework questions](#Homework-questions)
#   1. [Different model factory [1 points]](#Different-model-factory-[1-points])
#   1. [Directional unigram features [1.5 points]](#Directional-unigram-features-[1.5-points])
#   1. [The part-of-speech tags of the "middle" words [1.5 points]](#The-part-of-speech-tags-of-the-"middle"-words-[1.5-points])
#   1. [Bag of Synsets [2 points]](#Bag-of-Synsets-[2-points])
#   1. [Your original system [3 points]](#Your-original-system-[3-points])
# 1. [Bake-off [1 point]](#Bake-off-[1-point])

# ## Overview
# 
# This homework and associated bake-off are devoted to developing really effective relation extraction systems using distant supervision. 
# 
# As with the previous assignments, this notebook first establishes a baseline system. The initial homework questions ask you to create additional baselines and suggest areas for innovation, and the final homework question asks you to develop an original system for you to enter into the bake-off.

# ## Set-up
# 
# See [the first notebook in this unit](rel_ext_01_task.ipynb#Set-up) for set-up instructions.

# In[2]:


import numpy as np
import os
import rel_ext
from sklearn.linear_model import LogisticRegression
import utils


# As usual, we unite our corpus and KB into a dataset, and create some splits for experimentation:

# In[3]:


rel_ext_data_home = os.path.join('data', 'rel_ext_data')


# In[4]:


corpus = rel_ext.Corpus(os.path.join(rel_ext_data_home, 'corpus.tsv.gz'))


# In[5]:


kb = rel_ext.KB(os.path.join(rel_ext_data_home, 'kb.tsv.gz'))


# In[6]:


dataset = rel_ext.Dataset(corpus, kb)


# You are not wedded to this set-up for splits. The bake-off will be conducted on a previously unseen test-set, so all of the data in `dataset` is fair game:

# In[7]:


splits = dataset.build_splits(
    split_names=['tiny', 'train', 'dev'],
    split_fracs=[0.01, 0.79, 0.20],
    seed=1)


# In[8]:


splits


# ## Baselines

# ### Hand-build feature functions

# In[9]:


def simple_bag_of_words_featurizer(kbt, corpus, feature_counter):
    for ex in corpus.get_examples_for_entities(kbt.sbj, kbt.obj):
        for word in ex.middle.split(' '):
            feature_counter[word] += 1
    for ex in corpus.get_examples_for_entities(kbt.obj, kbt.sbj):
        for word in ex.middle.split(' '):
            feature_counter[word] += 1
    return feature_counter


# In[10]:


featurizers = [simple_bag_of_words_featurizer]


# In[11]:


model_factory = lambda: LogisticRegression(fit_intercept=True, solver='liblinear')


# In[12]:


baseline_results = rel_ext.experiment(
    splits,
    train_split='train',
    test_split='dev',
    featurizers=featurizers,
    model_factory=model_factory,
    verbose=True)


# Studying model weights might yield insights:

# In[13]:


rel_ext.examine_model_weights(baseline_results)


# ### Distributed representations
# 
# This simple baseline sums the GloVe vector representations for all of the words in the "middle" span and feeds those representations into the standard `LogisticRegression`-based `model_factory`. The crucial parameter that enables this is `vectorize=False`. This essentially says to `rel_ext.experiment` that your featurizer or your model will do the work of turning examples into vectors; in that case, `rel_ext.experiment` just organizes these representations by relation type.

# In[14]:


GLOVE_HOME = os.path.join('data', 'glove.6B')


# In[15]:


glove_lookup = utils.glove2dict(
    os.path.join(GLOVE_HOME, 'glove.6B.300d.txt'))


# In[16]:


def glove_middle_featurizer(kbt, corpus, np_func=np.sum):
    reps = []
    for ex in corpus.get_examples_for_entities(kbt.sbj, kbt.obj):
        for word in ex.middle.split():
            rep = glove_lookup.get(word)
            if rep is not None:
                reps.append(rep)
    # A random representation of the right dimensionality if the
    # example happens not to overlap with GloVe's vocabulary:
    if len(reps) == 0:
        dim = len(next(iter(glove_lookup.values())))                
        return utils.randvec(n=dim)
    else:
        return np_func(reps, axis=0)


# In[17]:


glove_results = rel_ext.experiment(
    splits,
    train_split='train',
    test_split='dev',
    featurizers=[glove_middle_featurizer],    
    vectorize=False, # Crucial for this featurizer!
    verbose=True)


# With the same basic code design, one can also use the PyTorch models included in the course repo, or write new ones that are better aligned with the task. For those models, it's likely that the featurizer will just return a list of tokens (or perhaps a list of lists of tokens), and the model will map those into vectors using an embedding.

# ## Homework questions
# 
# Please embed your homework responses in this notebook, and do not delete any cells from the notebook. (You are free to add as many cells as you like as part of your responses.)

# ### Different model factory [1 points]
# 
# The code in `rel_ext` makes it very easy to experiment with other classifier models: one need only redefine the `model_factory` argument. This question asks you to assess a [Support Vector Classifier](https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html).
# 
# __To submit:__ A wrapper function `run_svm_model_factory` that does the following: 
# 
# 1. Uses `rel_ext.experiment` with the model factory set to one based in an `SVC` with `kernel='linear'` and all other arguments left with default values. 
# 1. Trains on the 'train' part of `splits`.
# 1. Assesses on the `dev` part of `splits`.
# 1. Uses `featurizers` as defined above. 
# 1. Returns the return value of `rel_ext.experiment` for this set-up.
# 
# The function `test_run_svm_model_factory` will check that your function conforms to these general specifications.

# In[18]:


from sklearn.svm import SVC

def run_svm_model_factory():
    experiment = rel_ext.experiment(splits, 
                                    train_split='train', 
                                    test_split='dev',
                                    featurizers=featurizers, 
                                    model_factory = (lambda: SVC(kernel='linear')))
    
    
    return experiment


# In[19]:


def test_run_svm_model_factory(run_svm_model_factory):
    results = run_svm_model_factory()
    assert 'featurizers' in results,         "The return value of `run_svm_model_factory` seems not to be correct"
    # Check one of the models to make sure it's an SVC:
    assert 'SVC' in results['models']['adjoins'].__class__.__name__,         "It looks like the model factor wasn't set to use an SVC."    


# In[20]:


if 'IS_GRADESCOPE_ENV' not in os.environ:
    test_run_svm_model_factory(run_svm_model_factory)


# ### Directional unigram features [1.5 points]
# 
# The current bag-of-words representation makes no distinction between "forward" and "reverse" examples. But, intuitively, there is big difference between _X and his son Y_ and _Y and his son X_. This question asks you to modify `simple_bag_of_words_featurizer` to capture these differences. 
# 
# __To submit:__
# 
# 1. A feature function `directional_bag_of_words_featurizer` that is just like `simple_bag_of_words_featurizer` except that it distinguishes "forward" and "reverse". To do this, you just need to mark each word feature for whether it is derived from a subject–object example or from an object–subject example.  The included function `test_directional_bag_of_words_featurizer` should help verify that you've done this correctly.
# 
# 2. A call to `rel_ext.experiment` with `directional_bag_of_words_featurizer` as the only featurizer. (Aside from this, use all the default values for `rel_ext.experiment` as exemplified above in this notebook.)
# 
# 3. `rel_ext.experiment` returns some of the core objects used in the experiment. How many feature names does the `vectorizer` have for the experiment run in the previous step? Include the code needed for getting this value. (Note: we're partly asking you to figure out how to get this value by using the sklearn documentation, so please don't ask how to do it!)

# In[54]:


def directional_bag_of_words_featurizer(kbt, corpus, feature_counter): 
    # Append these to the end of the keys you add/access in 
    # `feature_counter` to distinguish the two orders. You'll
    # need to use exactly these strings in order to pass 
    # `test_directional_bag_of_words_featurizer`.
    subject_object_suffix = "_SO"
    object_subject_suffix = "_OS"
    
    ##### YOUR CODE HERE
    
    for ex in corpus.get_examples_for_entities(kbt.sbj, kbt.obj):
        for word in ex.middle.split(' '):
            word_w_suffix = word + subject_object_suffix
            feature_counter[word_w_suffix] += 1
    for ex in corpus.get_examples_for_entities(kbt.obj, kbt.sbj):
        for word in ex.middle.split(' '):
            word_w_suffix = word + object_subject_suffix
            feature_counter[word_w_suffix] += 1

    return feature_counter


# Call to `rel_ext.experiment`:
##### YOUR CODE HERE   
featurizers = [directional_bag_of_words_featurizer]

baseline_results = rel_ext.experiment(
    splits,
    train_split='train',
    test_split='dev',
    featurizers=featurizers,
    model_factory=model_factory,
    verbose=True)


# In[55]:


# Getting the number of features in the vectorizer, per Part3
vectorizer = baseline_results['vectorizer']
print(len(vectorizer.feature_names_))


# In[56]:


def test_directional_bag_of_words_featurizer(corpus):
    from collections import defaultdict
    kbt = rel_ext.KBTriple(rel='worked_at', sbj='Randall_Munroe', obj='xkcd')
    feature_counter = defaultdict(int)
    # Make sure `feature_counter` is being updated, not reinitialized:
    feature_counter['is_OS'] += 5
    feature_counter = directional_bag_of_words_featurizer(kbt, corpus, feature_counter)
    expected = defaultdict(
        int, {'is_OS':6,'a_OS':1,'webcomic_OS':1,'created_OS':1,'by_OS':1})
    assert feature_counter == expected,         "Expected:\n{}\nGot:\n{}".format(expected, feature_counter)


# In[57]:


if 'IS_GRADESCOPE_ENV' not in os.environ:
    test_directional_bag_of_words_featurizer(corpus)


# ### The part-of-speech tags of the "middle" words [1.5 points]
# 
# Our corpus distribution contains part-of-speech (POS) tagged versions of the core text spans. Let's begin to explore whether there is information in these sequences, focusing on `middle_POS`.
# 
# __To submit:__
# 
# 1. A feature function `middle_bigram_pos_tag_featurizer` that is just like `simple_bag_of_words_featurizer` except that it creates a feature for bigram POS sequences. For example, given 
# 
#   `The/DT dog/N napped/V`
#   
#    we obtain the list of bigram POS sequences
#   
#    `b = ['<s> DT', 'DT N', 'N V', 'V </s>']`. 
#    
#    Of course, `middle_bigram_pos_tag_featurizer` should return count dictionaries defined in terms of such bigram POS lists, on the model of `simple_bag_of_words_featurizer`.  Don't forget the start and end tags, to model those environments properly! The included function `test_middle_bigram_pos_tag_featurizer` should help verify that you've done this correctly.
# 
# 2. A call to `rel_ext.experiment` with `middle_bigram_pos_tag_featurizer` as the only featurizer. (Aside from this, use all the default values for `rel_ext.experiment` as exemplified above in this notebook.)

# In[191]:


def middle_bigram_pos_tag_featurizer(kbt, corpus, feature_counter):
    
    ##### YOUR CODE HERE
    pos_list = []
    for ex in corpus.get_examples_for_entities(kbt.sbj, kbt.obj):
        b = get_tag_bigrams(ex.middle_POS)
        pos_list.extend(b)
        
    for ex in corpus.get_examples_for_entities(kbt.obj, kbt.sbj):
        b = get_tag_bigrams(ex.middle_POS)
        pos_list.extend(b)
        
    for pos_tag in pos_list:
        feature_counter[pos_tag] += 1

    return feature_counter


def get_tag_bigrams(s):
    """Suggested helper method for `middle_bigram_pos_tag_featurizer`.
    This should be defined so that it returns a list of str, where each 
    element is a POS bigram."""
    # The values of `start_symbol` and `end_symbol` are defined
    # here so that you can use `test_middle_bigram_pos_tag_featurizer`.
    start_symbol = "<s>"
    end_symbol = "</s>"
    
    ##### YOUR CODE HERE
    b = []
    tags = get_tags(s)
    last_POS = '' 
    current_POS = start_symbol
    
    for tag in tags:
        last_POS = current_POS
        current_POS = tag
        bigram = last_POS + ' ' + current_POS
        b.append(bigram)
        
    # End symbol
    b.append(current_POS + ' ' + end_symbol)
        
    return b
    
def get_tags(s): 
    """Given a sequence of word/POS elements (lemmas), this function
    returns a list containing just the POS elements, in order.    
    """
    return [parse_lem(lem)[1] for lem in s.strip().split(' ') if lem]


def parse_lem(lem):
    """Helper method for parsing word/POS elements. It just splits
    on the rightmost / and returns (word, POS) as a tuple of str."""
    return lem.strip().rsplit('/', 1)  

# Call to `rel_ext.experiment`:
##### YOUR CODE HERE
featurizers = [middle_bigram_pos_tag_featurizer]

baseline_results = rel_ext.experiment(
    splits,
    train_split='train',
    test_split='dev',
    featurizers=featurizers,
    model_factory=model_factory,
    verbose=True)


# In[192]:


def test_middle_bigram_pos_tag_featurizer(corpus):
    from collections import defaultdict
    kbt = rel_ext.KBTriple(rel='worked_at', sbj='Randall_Munroe', obj='xkcd')
    feature_counter = defaultdict(int)
    # Make sure `feature_counter` is being updated, not reinitialized:
    feature_counter['<s> VBZ'] += 5
    feature_counter = middle_bigram_pos_tag_featurizer(kbt, corpus, feature_counter)
    expected = defaultdict(
        int, {'<s> VBZ':6,'VBZ DT':1,'DT JJ':1,'JJ VBN':1,'VBN IN':1,'IN </s>':1})
    assert feature_counter == expected,         "Expected:\n{}\nGot:\n{}".format(expected, feature_counter)


# In[193]:


if 'IS_GRADESCOPE_ENV' not in os.environ:
    test_middle_bigram_pos_tag_featurizer(corpus)


# ### Bag of Synsets [2 points]
# 
# The following allows you to use NLTK's WordNet API to get the synsets compatible with _dog_ as used as a noun:
# 
# ```
# from nltk.corpus import wordnet as wn
# dog = wn.synsets('dog', pos='n')
# dog
# [Synset('dog.n.01'),
#  Synset('frump.n.01'),
#  Synset('dog.n.03'),
#  Synset('cad.n.01'),
#  Synset('frank.n.02'),
#  Synset('pawl.n.01'),
#  Synset('andiron.n.01')]
# ```
# 
# This question asks you to create synset-based features from the word/tag pairs in `middle_POS`.
# 
# __To submit:__
# 
# 1. A feature function `synset_featurizer` that is just like `simple_bag_of_words_featurizer` except that it returns a list of synsets derived from `middle_POS`. Stringify these objects with `str` so that they can be `dict` keys. Use `convert_tag` (included below) to convert tags to `pos` arguments usable by `wn.synsets`. The included function `test_synset_featurizer` should help verify that you've done this correctly.
# 
# 2. A call to `rel_ext.experiment` with `synset_featurizer` as the only featurizer. (Aside from this, use all the default values for `rel_ext.experiment`.)

# In[222]:


from nltk.corpus import wordnet as wn

def synset_featurizer(kbt, corpus, feature_counter):
    
    ##### YOUR CODE HERE
    synsets = []
    for ex in corpus.get_examples_for_entities(kbt.sbj, kbt.obj):
        synsets.extend(get_synsets(ex.middle_POS))

        
    for ex in corpus.get_examples_for_entities(kbt.obj, kbt.sbj):
        synsets.extend(get_synsets(ex.middle_POS))
        
    for s in synsets:
        feature_counter[s] += 1
        
    return feature_counter


def get_synsets(s):
    """Suggested helper method for `synset_featurizer`. This should
    be completed so that it returns a list of stringified Synsets 
    associated with elements of `s`.
    """   
    # Use `parse_lem` from the previous question to get a list of
    # (word, POS) pairs. Remember to convert the POS strings.
    wt = [parse_lem(lem) for lem in s.strip().split(' ') if lem]
    
    ##### YOUR CODE HERE
    r = []
    for word_POS in wt:
        tag = convert_tag(word_POS[1])
        
        # We want to "stringify" each individual synset to be a feature.
        synsets = wn.synsets(word_POS[0], tag)
        for synset in synsets:
            r.append(str(synset))
    
    return r
    
    
def convert_tag(t):
    """Converts tags so that they can be used by WordNet:
    
    | Tag begins with | WordNet tag |
    |-----------------|-------------|
    | `N`             | `n`         |
    | `V`             | `v`         |
    | `J`             | `a`         |
    | `R`             | `r`         |
    | Otherwise       | `None`      |
    """        
    if t[0].lower() in {'n', 'v', 'r'}:
        return t[0].lower()
    elif t[0].lower() == 'j':
        return 'a'
    else:
        return None    


# Call to `rel_ext.experiment`:
##### YOUR CODE HERE    
featurizers = [synset_featurizer]

baseline_results = rel_ext.experiment(
    splits,
    train_split='train',
    test_split='dev',
    featurizers=featurizers,
    model_factory=model_factory,
    verbose=True)


# In[223]:


def test_synset_featurizer(corpus):
    from collections import defaultdict
    kbt = rel_ext.KBTriple(rel='worked_at', sbj='Randall_Munroe', obj='xkcd')
    feature_counter = defaultdict(int)
    # Make sure `feature_counter` is being updated, not reinitialized:
    feature_counter["Synset('be.v.01')"] += 5
    feature_counter = synset_featurizer(kbt, corpus, feature_counter)
    # The full return values for this tend to be long, so we just
    # test a few examples to avoid cluttering up this notebook.
    test_cases = {
        "Synset('be.v.01')": 6,
        "Synset('embody.v.02')": 1
    }
    for ss, expected in test_cases.items():   
        result = feature_counter[ss]
        assert result == expected,             "Incorrect count for {}: Expected {}; Got {}".format(ss, expected, result)


# In[224]:


if 'IS_GRADESCOPE_ENV' not in os.environ:
    test_synset_featurizer(corpus)


# ### Your original system [3 points]
# 
# There are many options, and this could easily grow into a project. Here are a few ideas:
# 
# - Try out different classifier models, from `sklearn` and elsewhere.
# - Add a feature that indicates the length of the middle.
# - Augment the bag-of-words representation to include bigrams or trigrams (not just unigrams).
# - Introduce features based on the entity mentions themselves. <!-- \[SPOILER: it helps a lot, maybe 4% in F-score. And combines nicely with the directional features.\] -->
# - Experiment with features based on the context outside (rather than between) the two entity mentions — that is, the words before the first mention, or after the second.
# - Try adding features which capture syntactic information, such as the dependency-path features used by Mintz et al. 2009. The [NLTK](https://www.nltk.org/) toolkit contains a variety of [parsing algorithms](http://www.nltk.org/api/nltk.parse.html) that may help.
# - The bag-of-words representation does not permit generalization across word categories such as names of people, places, or companies. Can we do better using word embeddings such as [GloVe](https://nlp.stanford.edu/projects/glove/)?
# 
# In the cell below, please provide a brief technical description of your original system, so that the teaching team can gain an understanding of what it does. This will help us to understand your code and analyze all the submissions to identify patterns and strategies.

# In[246]:


# Enter your system description in this cell.

# all featurizers - LR - f-score MA 0.615
# all featurizers - RF - 100/250/400 trees - f-score MA 0.749 - 0.754
# all featurizers - RF - oob_score - f-score MA 0.749

# My best system was just the base random forests implementation in scikit learn ran on all of the featurizers
# in this notebook except for the glove one. Tuning the RF implementation gave me no gains whatsoever.
# To get more accuracy we likely need more featurizers and more data. An observation while training and 
# doing a hyperparameter search is that recall is especially low here. We could tune the threshold for
# classification and probably raise our auprc.

# My peak score was: 0.754
# This is my code
if 'IS_GRADESCOPE_ENV' not in os.environ:
    from sklearn.ensemble import RandomForestClassifier
    featurizers = [simple_bag_of_words_featurizer, directional_bag_of_words_featurizer, middle_bigram_pos_tag_featurizer, synset_featurizer]
    model_factory = lambda: RandomForestClassifier(verbose=3, n_jobs=-1)
    default_rf = rel_ext.experiment(
        splits,
        train_split='train',
        test_split='dev',
        featurizers=featurizers,
        model_factory=model_factory,
        verbose=True)

# Please do not remove this comment.


# ## Bake-off [1 point]
# 
# For the bake-off, we will release a test set. The announcement will go out on the discussion forum. You will evaluate your custom model from the previous question on these new datasets using the function `rel_ext.bake_off_experiment`. Rules:
# 
# 1. Only one evaluation is permitted.
# 1. No additional system tuning is permitted once the bake-off has started.
# 
# The cells below this one constitute your bake-off entry.
# 
# People who enter will receive the additional homework point, and people whose systems achieve the top score will receive an additional 0.5 points. We will test the top-performing systems ourselves, and only systems for which we can reproduce the reported results will win the extra 0.5 points.
# 
# Late entries will be accepted, but they cannot earn the extra 0.5 points. Similarly, you cannot win the bake-off unless your homework is submitted on time.
# 
# The announcement will include the details on where to submit your entry.

# In[ ]:


# Enter your bake-off assessment code in this cell. 
# Please do not remove this comment.
if 'IS_GRADESCOPE_ENV' not in os.environ:
    pass
    # Please enter your code in the scope of the above conditional.
    ##### YOUR CODE HERE



# In[ ]:


# On an otherwise blank line in this cell, please enter
# your macro-average f-score (an F_0.5 score) as reported 
# by the code above. Please enter only a number between 
# 0 and 1 inclusive. Please do not remove this comment.
if 'IS_GRADESCOPE_ENV' not in os.environ:
    pass
    # Please enter your score in the scope of the above conditional.
    ##### YOUR CODE HERE


