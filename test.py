import kenlm

model = kenlm.Model('language_model/4-gram-lower.arpa')
print(model.score('this is a sentence .', bos = True, eos=True))