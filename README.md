# ETF EASY
#### Video Demo:  <URL HERE>
#### Description:
1. Project Description: <br/>
    My application is a portfolio management system. Its target customers are inexperienced investors and the goal is to give them a simple possibility to manage there portfolio with an easy to understand and transparent strategy. Because the target customers are assumed to be inexperienced, the underlying instruments should be ETFs as they are diversified instruments opposed to individual stocks and therefore having less underlying risk. Though it would be possible to use the application for managing individual shares as well.<br/>
    It supports three types of risk views, the first is the risk averse view, the second the balanced risk view and the third the risk seeking view. This means depending on the risk view of the customer, he/she can use different portfolio management strategies. E.g., the risk averse person will choose to invest his money in 70% of a riskless component and 30% in a more risky component, the balanced risk view of a person will invest 50% in a riskless component and 50% in a more risky component and finally the risk seeking person will invest only 30% of a riskless component and most of his money , i.e., 70%; in a more risky component. By saying riskless component an ETF with underlying fixed income instruments is meant and with a more risky component an ETF with shares as underlying are meant (it is clear that also the riskless component has inherent risk).<br/>
    Because this application is self managed by the user, he/she needs to decide what is defined to be a riskless ETF and what is defined to be a risky ETF. This is done when the user sets up his position by buying certain ETFs and defining him-/herself if the riskiness is High or Low.<br/>
    After login, which means you have to first register yourself, the user is led to the index page, giving him/her an overview of his/her position. The user logged in is alerted when his position is out of range w.r.t. the thresholds connected to his/her chosen risk view (risk averse, balanced, risk seeking).  


2. Content of the implemented files: <br/>
    - **app.py**: flask file linking all files together
    - **FirstPage_ETF.html**: Landing Page of the user. Gives a short Description what the applications does and what is meant with ETF EASY - Portfoliomanagement, i.e. what is meant with portfolio management for a risk averse, balance or risk seeking view. Once the user has decided what type of person of view he/she wants to take the landing page directs you to register as risk avers, balanced or risk seeking person.
    - **login.html**: Once registered as risk avers, balanced or risk seeking the user has to log in with his username and password.
    - **index_ETF.html**: This page shows three tables.
        + ETF Position at Current Price
            - Symbol - The symbol of the ETF as used by yahoo financials.
            - Open Quantity - Shows how many ETFs are building the position, i.e. the open position.
            - Risk - Shows what riskiness was defined for this ETF, i.e. low or high.
            - Current Price - This price is taken from the Yahoo API implemented in this application.
            - Avg Cost – When buying a certain ETF at different point in times at different prices this shows the average price   paid.
            - Total Cost – Quantity * Avg Cost
            - Current Value – Open Quantity * Current Price
            - Unreal. PnL – The unrealized Profit and Loss is given by the difference Current Value – Total Costs.
            - Real. Pnl - The realized Pnl is given by (agerage sell price - average buy price) * sell quantity. 
        + Risk Position in $ and Percentage %
            - Low Risk Pos $: Here the values at current price for all ETF positions categorised as low are added up.
            - High Risk Pos $: Here the values at current price for all ETF positions categorised as high are added up.
            - Overall Low Pos %: Here the percentage portion of the low risk position in relation to the overall position is shown in %.
            - Overall High Pos %: Here the percentage portion of the high risk position in relation to the overall position is shown in %.
        + ETF Transaction ar Cost in $: Here every buy and sell transaction is listed.

    - buy_ETF.html: For buying an ETF of stock the symbol has to be entered and the user has to decide what category of risk, i.e. High or Low, the stock will be attached to. Eventually the user has to insert the quantity he/she wants ot buy at the current price. 

    - sell_ETF.html: For selling a drop down menue is available with the ETFs symbols available for selling. The user has to insert the quantity and the price he/she wants to sell the ETF.

    - quoted_ETF.html: This is an information page presenting the long name of an ETF with its symbol and current market price.
3. Design Choices: <br/>

    - Development Environment: I have chosen to set up my development environment on a linux Ubuntu system because it gives me more flexibility e.g. loading pictures and other items used by the webpage.

    - Bootstrap: I have chosen to download bootstrap on my development environment because it gives me the ability to manipulate the standards set up within bootstrap like e.g. the colors. Because I am using a picture/diagram developed in another tool called yEd Graph Editor used on the landing page visualizing the application and the processes and because this picture uses different colors than the once used in bootstrap as standard I decided to adjust the colors in bootstrap to match with the once used in the picture.

    - Financial Information: I have chosen to use the interface to yahoo financials as it gives a lot of information around financial instruments and most important also the current price of an ETF or stock on the market. Future enhancement using other financial information is possible

    - SQLITE3: Because the users position is based on individual transactions, i.e. buys and sells, they have to be stored and a database seems to be a good solution for this. Also the fact that a user has a certain risk type attached has to be permanently available once the user has logged in, therefore a database can establish this. 
