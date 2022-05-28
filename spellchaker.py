class SpellChecker:
    def __init__(self, input_text,
                 language='EN', extended_dictionary = False,
                 window=None, progress_bar_key=None):
        
        available_languages = ['EN']
        if language not in available_languages:
            raise Exception(f'Incorrect language. Available options: \
                            {", ".join(available_languages)}')
            
        word_dict_path = ('words.txt' if not extended_dictionary 
                          else 'words_extended.txt')
        with open(word_dict_path) as words_file:
            self.words_dict = [word.strip('\n') for word in words_file]
        self.input_text = [word for word in input_text.split(' ')]
        
        self.window = window if window else None
        self.progress_bar_key = progress_bar_key if progress_bar_key else None
            
            
    def check_text(self):
        corrections = []
        if self.progress_bar_key and self.window:
            self.window[self.progress_bar_key].update(visible=True)
            
        for word_index, word in enumerate(self.input_text):
            value_percent = (word_index+1) / len(self.input_text)
                
            current_word_corrections = []
            if word == '':
                self.update_progress_bar(value_percent)
                continue
            
            ends_with = ''
            is_capitalized = True if word[0].isupper() else False
            if word != 'I':
                word = word.lower()
            
            if word[-1] in ['.', ',', '!', '?', '-']:
                ends_with = word[-1]
                word = word[:-1]
                
            if word in self.words_dict or word.isnumeric():
                corrections.append(current_word_corrections)
                self.update_progress_bar(value_percent)
                continue
            
            best_distance = self.calc_edit_distance(word, self.words_dict[0])
            distances = {}
            
            for w in self.words_dict:
                distances[w] = self.calc_edit_distance(word, w)
            
            best_distance = min(distances.values())
            for w, v in distances.items():
                if v == best_distance:
                    if is_capitalized:
                        current_word_corrections.append(w.capitalize() + ends_with)
                    else:
                        current_word_corrections.append(w + ends_with)
            corrections.append(current_word_corrections)
            self.update_progress_bar(value_percent)
        return corrections
    
    
    def update_progress_bar(self, percent):
        if self.progress_bar_key and self.window:
            self.window[self.progress_bar_key].update(current_count=percent*50)
        
        
    def calc_edit_distance(self, word1, word2):
        distance_table = [[None for _ in range(len(word1)+1)]
                          for __ in range(len(word2)+1)]
        for i in range(len(word1)+1):
            distance_table[0][i] = i
        
        for i in range(len(word2)+1):
            distance_table[i][0] = i
            
        for i in range(1, len(distance_table)):
            for j in range(1, len(distance_table[i])):
                
                if word2[i-1] == word1[j-1]:
                    distance_table[i][j] = distance_table[i-1][j-1]
                else:
                    distance_table[i][j] = min(distance_table[i][j-1],
                                               distance_table[i-1][j],
                                               distance_table[i-1][j-1]) \
                                           +1
        return distance_table[-1][-1]