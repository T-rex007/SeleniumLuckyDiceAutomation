# Dice Game Bot
<p>
This is a commmand line operated automated bot, that was built using Selenium, OpenCV and Pytesseract to play an online gambling Game called Lucky Dice.
</p>


<br>
<br>

<img src="ReadMe-files\Lucky Dice.png" alt="LuckyDice" style="vertical-align:middle">
<br>
<br>

## Setup 
<br>
<ul>
    <li>Install python</li>
    <li>Install anaconda</li>
    <li>Create a conda enviroment<br> 
    <code>conda create --name "enviroment-name" --file requirements.txt</code>
    </li>

</ul>

## How to run? 

In the Terminal You must first Navigate to the folder when program is located. For Instance

<br>
<code>cd ..</code>
<br>
This will take you to the root directory and from here you will need to change the director to the directory of the program using 
<br>
<code>cd PATH </code>
<br>
For instance
<br>
<code>cd LuckyDice/SeleniumLuckyDiceAutomation-master</code>
<br>
Then activate virtual Environment using
<code>conda activate Environment_Name</code>
<br>
Example:
<br>
<code>conda activate LuckyDice</code>
<br>
If by chance you have forgotten the name of the enviromentfor this program, is you can see a list of t enviroments on the systme by using the command
<br>
<code>conda info --envs</code>
<br>
Or
<br>
<code>cond env list</code>



### To run program in testing mode (input parmeters specified  in code only)
<code>python bot.py test</code>
<br> 
### To run program in live mode (Where actual money is spent)
<code>python bot.py live</code>
<br>  
### To run the program in demo mode (Ran in dome mode where user input in accepted)
<code>python bot.py demo</code>

<style>
code {
  font-family: Consolas,"courier new";
  color: crimson;
  background-color: #f1f1f1;
  padding: 2px;
  font-size: 105%;
}
</style>
