"""Demo agent that analyzes news sentiment and trends with enterprise-grade features."""

import asyncio
import logging
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Tuple
import re
from collections import Counter

# ANSI color codes for formatted output
CYAN = '\033[0;36m'
GREEN = '\033[0;32m'
YELLOW = '\033[0;33m'
RED = '\033[0;31m'
NC = '\033[0m'  # No Color

class NewsAgent:
    """Agent that demonstrates enterprise-grade text processing and sentiment analysis"""
    
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
        """Generate demo news articles with realistic variations"""
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
            # Generate article text with more variety
            words = headline.split()
            article = f"{headline}. "
            
            if "Strong" in headline or "Surges" in headline:
                article += f"The company's performance has exceeded market expectations, showing robust growth in key metrics. "
                article += f"Investors are responding positively to {symbol}'s strategic initiatives. "
            elif "Concerns" in headline or "Warn" in headline:
                article += f"Market analysts express caution about {symbol}'s current trajectory. "
                article += "The company faces multiple challenges in an evolving market landscape. "
            else:
                article += f"The impact on {symbol}'s market position remains to be seen. "
                article += "Industry experts are closely monitoring these developments. "
            
            news_items.append({
                "headline": headline,
                "content": article,
                "timestamp": (now - timedelta(days=day_offset)).isoformat(),
                "source": "Demo News Network"
            })
        
        return news_items

    def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze text sentiment with enhanced accuracy"""
        text = text.lower()
        words = re.findall(r'\w+', text)
        
        sentiment_score = 0
        sentiment_words = []
        
        # Track word proximity for context
        word_positions = {}
        for i, word in enumerate(words):
            if word in self.sentiment_words["positive"]:
                score = self.sentiment_words["positive"][word]
                sentiment_score += score
                sentiment_words.append((word, score))
                word_positions[word] = i
            elif word in self.sentiment_words["negative"]:
                score = self.sentiment_words["negative"][word]
                sentiment_score += score
                sentiment_words.append((word, score))
                word_positions[word] = i
        
        # Normalize score to [-1, 1] range
        if sentiment_words:
            sentiment_score /= len(sentiment_words)
        
        return {
            "score": sentiment_score,
            "words": sentiment_words,
            "magnitude": abs(sentiment_score),
            "label": "positive" if sentiment_score > 0.2 else "negative" if sentiment_score < -0.2 else "neutral"
        }

    def _extract_topics(self, text: str) -> List[Tuple[str, int]]:
        """Extract main topics with improved relevance"""
        # Enhanced stopwords list
        stopwords = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", 
            "for", "of", "with", "by", "from", "up", "about", "into", "over",
            "after", "has", "been", "was", "were", "will", "would", "could",
            "should", "than", "then", "that", "this", "these", "those"
        }
        
        # Extract phrases (basic implementation)
        text = text.lower()
        phrases = re.findall(r'\w+(?:\s+\w+){0,2}', text)  # Get up to 3-word phrases
        
        # Count meaningful phrases/words
        word_counts = Counter()
        for phrase in phrases:
            words = phrase.split()
            if all(word not in stopwords and len(word) > 3 for word in words):
                word_counts[phrase] += 1
        
        # Return top topics
        return word_counts.most_common(5)

    async def analyze_news(
        self,
        symbol: str,
        days: int = 7
    ) -> Dict[str, Any]:
        """Analyze news with enterprise-grade processing and error handling"""
        try:
            print(f"""
╔══════════════════════════════════════════════════════════════════╗
║  📰 NEWS ANALYSIS SYSTEM v1.0
║     ANALYZING {symbol}...
╚══════════════════════════════════════════════════════════════════╝

{CYAN}▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
📡 FETCHING NEWS DATA
🧮 SENTIMENT ANALYSIS: READY
📊 TOPIC EXTRACTION: READY
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀{NC}
""")
            
            print(f"{GREEN}[NEWS] Phase 1: Data Collection{NC}")
            self.log.info(f"Collecting news data for {symbol}")
            
            # Get demo news data
            news_items = self._generate_demo_news(symbol, days)
            print("✅ News data retrieved\n")
            
            print(f"{GREEN}[NEWS] Phase 2: Sentiment Analysis{NC}")
            print("🧠 Processing sentiment patterns...")
            
            # Analyze each article
            analyzed_items = []
            overall_sentiment = 0
            all_topics = Counter()
            
            for i, item in enumerate(news_items, 1):
                print(f"  📄 Analyzing article {i}/{len(news_items)}...")
                
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
            
            print("✅ Sentiment analysis complete\n")
            
            # Calculate overall metrics
            overall_sentiment /= len(news_items)
            
            print(f"{GREEN}[NEWS] Phase 3: Topic Analysis{NC}")
            print("🔍 Extracting key topics and trends...")
            print("✅ Topic analysis complete\n")
            
            print(f"""
{CYAN}▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
✨ ANALYSIS COMPLETE
📊 INSIGHTS GENERATED
🎯 READY FOR DISPLAY
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀{NC}
""")
            
            return {
                "status": "success",
                "data": {
                    "symbol": symbol,
                    "period_days": days,
                    "articles": analyzed_items,
                    "summary": {
                        "overall_sentiment": overall_sentiment,
                        "sentiment_label": "positive" if overall_sentiment > 0.2 else "negative" if overall_sentiment < -0.2 else "neutral",
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
        """Format news analysis with enhanced visual presentation"""
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
        
        # Get sentiment color and emoji
        if summary["overall_sentiment"] > 0.2:
            sentiment_color = GREEN
            sentiment_emoji = "🟢"
        elif summary["overall_sentiment"] < -0.2:
            sentiment_color = RED
            sentiment_emoji = "🔴"
        else:
            sentiment_color = YELLOW
            sentiment_emoji = "🟡"
        
        # Format topics with counts
        topics_str = ""
        for topic, count in summary["top_topics"]:
            bar_length = min(20, count * 2)  # Scale bar length
            bar = "█" * bar_length
            topics_str += f"    • {topic:<20} {bar} ({count} mentions)\n"
        
        # Format recent articles with colored sentiment
        articles_str = ""
        for article in data["articles"][:3]:  # Show 3 most recent
            sentiment = article["sentiment"]
            if sentiment["score"] > 0.2:
                color = GREEN
                emoji = "🟢"
            elif sentiment["score"] < -0.2:
                color = RED
                emoji = "🔴"
            else:
                color = YELLOW
                emoji = "🟡"
                
            articles_str += f"""
  • {article['headline']}
    Sentiment: {color}{emoji} {sentiment['label'].upper()} ({sentiment['score']:.2f}){NC}
    Key Topics: {', '.join(topic for topic, _ in article['topics'][:3])}
    Time: {article['timestamp']}
"""
        
        return f"""
╔══════════════════════════════════════════════════════════════════╗
║  📰 News Analysis - {data['symbol']}
╚══════════════════════════════════════════════════════════════════╝

📊 Analysis Summary:
  • Period: Last {data['period_days']} days
  • Articles Analyzed: {summary['article_count']}
  • Overall Sentiment: {sentiment_color}{sentiment_emoji} {summary['sentiment_label'].upper()} ({summary['overall_sentiment']:.2f}){NC}

🔍 Trending Topics:
{topics_str}
📑 Recent Coverage:{articles_str}

⏰ Last Updated: {result['timestamp']}
"""

async def main():
    """Run the NewsAgent demo with enterprise-grade setup"""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    agent = NewsAgent()
    
    # Demo with major tech companies
    symbols = ["AAPL", "GOOGL", "MSFT", "AMZN", "META"]
    
    for symbol in symbols:
        try:
            result = await agent.analyze_news(symbol)
            print(agent.format_output(result))
            await asyncio.sleep(1)  # Pause between demos
        except Exception as e:
            logging.error(f"Error processing {symbol}: {str(e)}")
            continue

if __name__ == "__main__":
    asyncio.run(main())
