"""Demo agent that analyzes news sentiment and trends."""

import asyncio
import logging
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Tuple
import re
from collections import Counter

class NewsAgent:
    """Agent that demonstrates text processing and sentiment analysis"""
    
    def __init__(self):
        self.log = logging.getLogger("demos.news_agent")
        self.name = "news_agent"
        
        # Demo sentiment words (replace with proper NLP model)
        self.sentiment_words = {
            "positive": {
                "surge": 0.8, "gain": 0.6, "up": 0.4, "rise": 0.6, "growth": 0.7,
                "profit": 0.8, "success": 0.9, "positive": 0.7, "strong": 0.6,
                "boost": 0.7, "improve": 0.6, "advantage": 0.7, "benefit": 0.6
            },
            "negative": {
                "drop": -0.7, "fall": -0.6, "down": -0.4, "decline": -0.6,
                "loss": -0.8, "risk": -0.6, "weak": -0.5, "negative": -0.7,
                "concern": -0.5, "worry": -0.6, "problem": -0.7, "crisis": -0.9
            }
        }

    def _generate_demo_news(self, symbol: str, days: int = 7) -> List[Dict[str, Any]]:
        """Generate demo news articles"""
        headlines = [
            (0, f"{symbol} Reports Strong Quarterly Earnings, Exceeding Expectations"),
            (1, f"Market Concerns Over {symbol}'s Growth Strategy"),
            (2, f"{symbol} Announces New Product Launch, Stock Surges"),
            (3, f"Analysts Warn of Potential Risks in {symbol}'s Expansion Plans"),
            (4, f"{symbol} Partners with Tech Giant for Innovation Boost"),
            (5, f"Industry Competition Poses Challenge to {symbol}'s Market Share"),
            (6, f"{symbol} Shows Positive Growth Trends Despite Market Pressure")
        ]
        
        news_items = []
        now = datetime.now(timezone.utc)
        
        for day_offset, (_, headline) in enumerate(headlines[:days]):
            # Generate article text
            words = headline.split()
            article = f"{headline}. "
            article += "The company's performance has been "
            article += "showing positive signs. " if day_offset % 2 == 0 else "facing some challenges. "
            article += f"Investors are closely monitoring {symbol}'s developments. "
            article += "Market analysts remain optimistic. " if day_offset % 2 == 0 else "Some analysts express concerns. "
            
            news_items.append({
                "headline": headline,
                "content": article,
                "timestamp": (now - timedelta(days=day_offset)).isoformat(),
                "source": "Demo News Network"
            })
        
        return news_items

    def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze text sentiment"""
        text = text.lower()
        words = re.findall(r'\w+', text)
        
        sentiment_score = 0
        sentiment_words = []
        
        for word in words:
            if word in self.sentiment_words["positive"]:
                score = self.sentiment_words["positive"][word]
                sentiment_score += score
                sentiment_words.append((word, score))
            elif word in self.sentiment_words["negative"]:
                score = self.sentiment_words["negative"][word]
                sentiment_score += score
                sentiment_words.append((word, score))
        
        # Normalize score to [-1, 1] range
        if sentiment_words:
            sentiment_score /= len(sentiment_words)
        
        return {
            "score": sentiment_score,
            "words": sentiment_words,
            "magnitude": abs(sentiment_score),
            "label": "positive" if sentiment_score > 0 else "negative" if sentiment_score < 0 else "neutral"
        }

    def _extract_topics(self, text: str) -> List[Tuple[str, int]]:
        """Extract main topics from text"""
        # Simple keyword extraction (replace with proper NLP)
        words = re.findall(r'\w+', text.lower())
        stopwords = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}
        
        # Count meaningful words
        word_counts = Counter(word for word in words if word not in stopwords and len(word) > 3)
        
        # Return top topics
        return word_counts.most_common(5)

    async def analyze_news(
        self,
        symbol: str,
        days: int = 7
    ) -> Dict[str, Any]:
        """Analyze news for a stock symbol"""
        try:
            self.log.info(f"Analyzing news for {symbol}")
            
            # Get demo news data
            news_items = self._generate_demo_news(symbol, days)
            
            # Analyze each article
            analyzed_items = []
            overall_sentiment = 0
            all_topics = Counter()
            
            for item in news_items:
                # Combine headline and content for analysis
                full_text = f"{item['headline']} {item['content']}"
                
                # Analyze sentiment
                sentiment = self._analyze_sentiment(full_text)
                overall_sentiment += sentiment["score"]
                
                # Extract topics
                topics = self._extract_topics(full_text)
                for topic, count in topics:
                    all_topics[topic] += count
                
                analyzed_items.append({
                    **item,
                    "sentiment": sentiment,
                    "topics": topics
                })
            
            # Calculate overall metrics
            overall_sentiment /= len(news_items)
            
            return {
                "status": "success",
                "data": {
                    "symbol": symbol,
                    "period_days": days,
                    "articles": analyzed_items,
                    "summary": {
                        "overall_sentiment": overall_sentiment,
                        "sentiment_label": "positive" if overall_sentiment > 0 else "negative" if overall_sentiment < 0 else "neutral",
                        "top_topics": all_topics.most_common(5),
                        "article_count": len(news_items)
                    }
                },
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
        except Exception as e:
            self.log.error(f"Error analyzing news: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }

    def format_output(self, result: Dict[str, Any]) -> str:
        """Format news analysis for display"""
        if result["status"] != "success":
            return f"""
╔══════════════════════════════════════════════════════════════════╗
║  ❌ News Analysis Error
╚══════════════════════════════════════════════════════════════════╝

Error: {result.get('error', 'Unknown error')}
Timestamp: {result['timestamp']}
"""
        
        data = result["data"]
        summary = data["summary"]
        
        # Get sentiment emoji
        sentiment_emoji = "🟢" if summary["overall_sentiment"] > 0.2 else "🔴" if summary["overall_sentiment"] < -0.2 else "⚪"
        
        # Format topics
        topics_str = "\n".join(f"    • {topic}: {count} mentions" for topic, count in summary["top_topics"])
        
        # Format recent articles
        articles_str = ""
        for article in data["articles"][:3]:  # Show 3 most recent
            sentiment = article["sentiment"]
            sentiment_label = "🟢 POSITIVE" if sentiment["score"] > 0.2 else "🔴 NEGATIVE" if sentiment["score"] < -0.2 else "⚪ NEUTRAL"
            articles_str += f"""
  • {article['headline']}
    Sentiment: {sentiment_label} ({sentiment['score']:.2f})
    Time: {article['timestamp']}
"""
        
        return f"""
╔══════════════════════════════════════════════════════════════════╗
║  📰 News Analysis - {data['symbol']}
╚══════════════════════════════════════════════════════════════════╝

📊 Summary:
  • Period: Last {data['period_days']} days
  • Articles Analyzed: {summary['article_count']}
  • Overall Sentiment: {sentiment_emoji} {summary['sentiment_label'].upper()} ({summary['overall_sentiment']:.2f})

🔍 Top Topics:
{topics_str}

📑 Recent Articles:{articles_str}

⏰ Last Updated: {result['timestamp']}
"""

async def main():
    """Demo the news agent"""
    agent = NewsAgent()
    
    # Demo stocks
    symbols = ["AAPL", "GOOGL", "MSFT", "AMZN"]
    
    for symbol in symbols:
        result = await agent.analyze_news(symbol)
        print(agent.format_output(result))
        await asyncio.sleep(1)  # Pause between demos

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())