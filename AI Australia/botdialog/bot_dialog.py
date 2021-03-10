from botbuilder.core import TurnContext,ActivityHandler,ConversationState,MessageFactory
from botbuilder.dialogs import DialogSet,WaterfallDialog,WaterfallStepContext
from botbuilder.dialogs.prompts import TextPrompt,NumberPrompt,PromptOptions, PromptValidatorContext 
from .FuelAnalysis import FuelAnalysis
class BotDialog(ActivityHandler):
    def __init__(self, fanlysis:FuelAnalysis,conversation:ConversationState):
        self.con_statea = conversation
        self.fAnalysis = fanlysis
        self.state_prop = self.con_statea.create_property("dialog_set")
        self.dialog_set = DialogSet(self.state_prop)
        self.dialog_set.add(NumberPrompt("number_prompt", self.IsValidAreaCode))
        self.dialog_set.add(WaterfallDialog("main_dialog",[self.GetIntro,self.GetCheapestCurrentPrice]))

    async def IsValidAreaCode(self,prompt_valid:PromptValidatorContext):
        if(prompt_valid.recognized.succeeded is False):
            await prompt_valid.context.send_activity("Please enter valid number")
            return False
        else:
            value = str(prompt_valid.recognized.value)
            if not(self.fAnalysis.checkPostCode(value)) :
                await prompt_valid.context.send_activity("Area Code invalid. Please try Again")
                return False
        return True

        
    async def GetIntro(self,waterfall_step:WaterfallStepContext):
        #return await waterfall_step._turn_context.send_activity("Welcome to Petrol Station locator.\n\nPlease enter area code to search")
        return await waterfall_step.prompt("number_prompt",PromptOptions(prompt=MessageFactory.text("Welcome to Petrol Station locator.\n\nPlease enter area code to search")))


    #async def GetAreaCode(self,waterfall_step:WaterfallStepContext):
     #   return await waterfall_step.prompt("number_prompt",PromptOptions(prompt=MessageFactory.text("Please enter area code to search")))
                
    async def GetCheapestCurrentPrice(self,waterfall_step:WaterfallStepContext):
        areacode = waterfall_step._turn_context.activity.text
        waterfall_step.values["code"] = areacode

        areacode = int(areacode)
        address,Price = self.fAnalysis.getInfo(areacode)  
        bday1,bday2,bbrand1 = self.fAnalysis.getBestDays(areacode)

        await waterfall_step._turn_context.send_activity("Address: "+str(address)+'\n\n'+" Price: "+str(Price)+"\n\n\n\n"+
        "Best Days to refuel:"+bday1+" and "+bday2+"\n\n"+"Cheapest Brand: "+bbrand1)
        return await waterfall_step.end_dialog()

   # async def GetBestDaysandBrands(self,waterfall_step:WaterfallStepContext):
    #    areacode = int(waterfall_step.values["code"] )
    #    await waterfall_step._turn_context.send_activity("Best Days to refuel:"+bday1+" and "+bday2+"\n\n"+"Cheapest Brand: "+bbrand1+" and "+bbrand2)
    #    return await waterfall_step.end_dialog()

        
    async def on_turn(self,turn_context:TurnContext):
        dialog_context = await self.dialog_set.create_context(turn_context)

        if(dialog_context.active_dialog is not None):
            await dialog_context.continue_dialog()
        else:
            await dialog_context.begin_dialog("main_dialog")
        
        await self.con_statea.save_changes(turn_context)