# Disclaimer

## Not Financial Advice

borsa is a software tool that aggregates and normalises publicly available market data. **Nothing in this software, its output, its documentation, or any associated materials constitutes financial, investment, legal, or tax advice.** Do not make investment decisions based solely on data returned by this service.

Always consult a qualified financial professional before making investment decisions. Past performance of any security is not indicative of future results.

## No Warranty

This software is provided **"as is"**, without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and non-infringement. In no event shall the authors or copyright holders be liable for any claim, damages, or other liability arising from the use of this software.

## Data Accuracy

borsa retrieves data from third-party providers (Alpha Vantage, Finnhub, Yahoo Finance). The authors of borsa:

- Make no guarantees about the accuracy, completeness, or timeliness of data returned by any provider
- Are not responsible for errors, omissions, or delays in provider data
- Do not independently verify any market data

Data may be delayed, incorrect, or unavailable without notice. Always cross-check critical data against official exchange sources (e.g., the [EGX website](https://www.egx.com.eg)).

## BYOK (Bring Your Own Key) Posture

borsa does not supply API keys and has no central server. You run your own instance and supply your own third-party API keys via environment variables. By using borsa you agree to the terms of service of each data provider whose key you configure or optional provider you enable:

- [Alpha Vantage Terms of Service](https://www.alphavantage.co/terms_of_service/)
- [Finnhub Terms of Service](https://finnhub.io/terms)
- [Yahoo Finance Terms](https://legal.yahoo.com/us/en/yahoo/terms/otos/index.html)

Compliance with provider rate limits, data redistribution restrictions, and permitted use policies is your responsibility.

Yahoo Finance support is implemented through the third-party `yfinance` package and is disabled by default in `.env.example`. Yahoo Finance/yfinance access is unofficial and may be limited to personal, research, or educational use depending on the applicable terms. Do not enable it for a public or commercial service unless you have confirmed that your intended use is permitted.

## Open Source Liability

The MIT licence under which borsa is distributed explicitly excludes any liability on the part of contributors. See [LICENSE](LICENSE) for the full terms.
