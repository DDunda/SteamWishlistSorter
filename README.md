# Steam Wishlist sorter
This little python script can help you order your wishlist. It simply calls a sort function and uses your responses to compare games. At the end it'll print a little table for you, showing your new order and how the ranks have changed.

Due to the time complexity of sorting algorithms you may be asked a lot of questions, e.g., ~70 for ~20 games. I tried to make answering as fast as possible, but sorting will always need many comparisons.

## How to use
Just run and follow the prompts.

You can find your username at your profile in the browser (e.g., DundaDunda in https://steamcommunity.com/id/DundaDunda), which will be used to grab your wishlist.

You can pre-sort it according to your current ranking (`m`, `mine`, `rank`, `order`), player reviews (`p`, `players`, `reviews`, `score`), or randomly (`r`, `random`, `shuffled`), which affects the order questions are asked. You can also choose to exclude unreleased games with `y`/`yes` or `n`/`no`.

I suggest using your ranking as it may be sorted well already, making everything quicker. Similarly, avoid random because it's random. It can reduce bias, but asks too many questions.

To compare games respond with `1`/`2`, `a`/`b`, or `l`/`r`; whichever you feel like. If it's a tossup use `?`/`=`, or just hit enter. Question and game numbers will be provided as you go to track your progress, because you're so, so slow >:)