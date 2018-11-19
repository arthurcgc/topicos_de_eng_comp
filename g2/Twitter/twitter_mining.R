library(twitteR)


consumer_key =    "o0nilhHquSu2VkWNXO3AR1f7W"
consumer_secret = "SMftjvttNth7L7aiCxNIHLhWAnu9PNQJ3zYGl7sEn61VqhiyGr"
access_token =    "1060111066976436224-buMwkpV71S0LQxwqhba2yBT1icHd5u"
access_secret = 	"7CTRCVqCuiBLfWWxbGLLJ19B4OKNKz1NaG1t2zUE5BK3T"

setup_twitter_oauth(consumer_key ,consumer_secret,access_token ,access_secret)


tweets = twitteR::searchTwitter("Politica",n =1000,lang ="pt",since = '2018-09-27')

df = twListToDF(tweets)
saveRDS(df, file="mytweets.rds")
df2 <- readRDS("mytweets.rds")

#clearing the
library(tm)
newdata<- iconv(df2$text, "ASCII", "UTF-8", sub="")
mydata <- Corpus(VectorSource(newdata))
removeURL <- function(x) gsub("http[^[:space:]]*", "", x)
mydata <- tm_map(mydata, content_transformer(removeURL))
removeNumPunct <- function(x) gsub("[^[:alpha:][:space:]]*", "", x)
mydata <- tm_map(mydata, content_transformer(removeNumPunct))
mydata <- tm_map(mydata, stripWhitespace)
mydata <- tm_map(mydata, removeNumbers)
mydata <- tm_map(mydata, removePunctuation)
mydataCopy <- mydata

#build a term document matrix
dtm <- TermDocumentMatrix(mydata)
m <- as.matrix(dtm)
v <- sort(rowSums(m),decreasing=TRUE)
d <- data.frame(word = names(v),freq=v)
head(d, 20)

#load the necessary libraries
library(wordcloud)
library(RColorBrewer)
#draw the word cloud
set.seed(1234)
wordcloud(words = d$word, freq = d$freq, min.freq = 20,max.words=500, random.order=FALSE,scale = c(3, 0.5), colors = rainbow(50))

barplot(d[1:40,]$freq, las = 2, names.arg = d[1:40,]$word,
        col ="blue", main ="Most frequent words",
        ylab = "Word frequencies")
