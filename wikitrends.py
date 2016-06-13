import wikipedia, sys

class WikiTrends:

    def __init__(self, article_name, limit=5):
        self.article = article_name                              # Name of article page in Wikipedia
        self.hits = []                                                     # Most frequent words in the article
        self.limit = limit                                               # Limit hits to the given number (default value is 5)

    def set_language(self, lang):                               # Change language of Wikipedia (default is English)
        wikipedia.set_lang(lang)

    def validate_article(self):                                    # Checks if article exists in Wikipedia
        try:
            if wikipedia.page(self.article).title:
                return True
        except:
            return False

    def get_hits(self, format='list'):
        word_dict = self.get_dict(self.article)             # Returns DICT with strings (key) and number of occurence (value)
        filter = self.get_banned_words(self.article)    # Words that we will be filtered from the top results

        for word in word_dict.keys():
            if word_dict[word] > 1 and word not in filter:
                self.hits.append((word_dict[word], word))
        result = sorted(self.hits, reverse=True)[:self.limit]
        if format is 'html':
            return str(self.get_html_hits(result))
        return result

    def get_html_hits(self, lst):
        result = ''
        for item in lst:
            result += str(item[1]) + ' (' + str(item[0]) + ' hits)<br />'
        return result

    def get_dict(self, article):
        article = wikipedia.page(article).content
        clean_article = self.get_clean_text(article).split()
        word_counts = self.get_stats(clean_article)
        return word_counts

    def get_clean_text(self, article):
        punctuations = ['.', ',', ':', ';', '(', ')', '?', '!', '<', '=', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        new_article = ''
        for i in range(len(article)):
                if article[i] not in punctuations:
                    new_article += article[i]
        return new_article.lower()

    def get_stats(self, article):
        statistics = {}
        for word in article:
            if word not in statistics.keys() and len(word) > 3:
                statistics[word] = self.get_occurence(article, word)
        return statistics #sorted(statistics)[:5]

    def get_occurence(self, article, keyword): # Get number of occurence of a specific word (keyword) in a string (article)
        count = 0
        for word in article:
            if word == keyword:
                count += 1
        return count

    def get_banned_words(self, article):
        return [self.article.lower(), 'with', 'from', 'also', 'which', 'under', 'that', 'were', 'between', 'their', 'first', 'been', 'other', 'this', 'born', 'many', 'most', 'large', 'have', 'they', 'than', 'more', 'such', 'largest', 'there', 'into', 'such', 'after', 'over', 'often', 'called', 'these', 'some', 'used', 'when', 'word', 'term']

if __name__ == "__main__":
    armenia = WikiTrends('Armenia', 10)
    print(armenia.get_hits('html'))
