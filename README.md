# KICKR Shifters

<img src="https://github.com/StephenDone/kickr_shifters/assets/68420912/0006cc02-046b-4ed4-8a2b-25e99c15ed23" width="324">

## About
This repository contains various projects around the shifters on the Waho KICKR indoor bike.

The aim is to provide sufficient information so that..
- anyone can build their own custom shifters - maybe you have a physical disability that makes standard shifters hard to use, or maybe you would just like to have tri-bar shifters on your bike.
- anyone can repair their shifters, once they are out of warranty or have been damaged in a way that voids the warranty.
- anyone can interface their bike's shifters to another device, promoting recycling and reuse of technology, once it reaches the end of its useful life.

## Documentation
See the [Wiki](../../wiki) for documentation. 

## Background
Ok, well here's a bit of a ramble to explain how this project came about and what it involves. I never actually set out to do this, though once I had, I thought it was worth documenting in case anyone else needs the information. 
I wanted to give tri bars a go indoors, to see if I could get used to the position. To do this, I wanted a second set of bars and shifters for my KICKR. This is because I have already swapped out the KICKR standard bars for some different bars which I prefer. Unfortunately, these bars do not have enough round bar clamp area to fit the tri bar clamps to. 
Eventually, I found some KICKR bars and shifters listed on eBay. Brand new apparently - great! They weren't. The cables were utterly f*#$*d!!! 
So I had to repair these shifters before I could use them. They had corroded connectors (both inside and out) and also intermittent breaks in the cabling along it's length... a proper mess. So first off, I had to source new connectors for the PCBs inside the shifters, and new connectors to plug into the KICKR itself. After that, I needed to make sure that my new cables were wired identically to the originals.
Opening up the shifters to get at the cables, I couldn't help but Google the chip on the board inside the shifters. The chip PDF was readily available and there just so happened to be a small cheap dev board available for it too. This sounded like a good excuse to dust off a Raspberry PI, write my first python script to test my repaired shifters, and also see if I could make some shifters to go in my tri-bars too. I didn't want to hurt my precious KICKR bike, which is now out of warranty - this was the most important thing. So I decided to make an adaptor to plug a KICKR shifter into my PI. I wrote a test script to talk to the £5 dev board first. I then made sure my PI works with the working shifters on my bike. I could then test that my repaired shifters also worked on my PI. If they did work, I could put the repaired shifters and tri bars on my bike, confident that all would be fine and they wouldn't hurt my precious KICKR. 

## Contact
If you have any feedback or ideas, or spot any errors, please contact me, preferably by creating an issue.

I take no responsibility for any damage that arises to your KICKR Bike, due to any errors in the information I have offered. Please verify any wiring, such as power supply polarity and pinouts as you go along - that's what I did. If you spot anything that is incorrect, please let me know.
