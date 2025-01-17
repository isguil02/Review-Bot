import discord
from discord.ext import commands
from discord import app_commands
import sqlite3
import ast
import math
import datetime



class ReviewCommands(commands.Cog):
    def __init__(self,bot):
        self.bot= bot
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{__name__} is online!")

    @app_commands.command(name="add_review",description="Give someone a review ")
    async def slash(self,interaction:discord.Interaction,member: discord.Member,rating_out_of_5:int,comment_under_150_characters:str,do_you_want_to_remain_anonymous:bool):
        rating=str(rating_out_of_5)
        memberId=str(member.id)
        member=str(member)
        comment=comment_under_150_characters
        userId=str(interaction.user.id)
        user=str(interaction.user)
        aboutC=""
        
        if member==user:
            await interaction.response.send_message(f"You can not review your self",ephemeral=True)
            return
        if rating_out_of_5>5 or rating_out_of_5 <0:
            await interaction.response.send_message(f"Please give a rating between 0-5",ephemeral=True)
            return
        if len(comment)>150:
            await interaction.response.send_message(f"Please shorten your comment",ephemeral=True)
            return
        if do_you_want_to_remain_anonymous==False:
            comment="Username:"+user+" Said -"+comment
            aboutC="This comment was wrote by User:"+user+" Id:"+userId
        else:
            comment="Anonymous Said -"+comment
            aboutC="The creator of this comment wants to stay anonymous."
        
        date = datetime.datetime.now()
        time = str(date.strftime("%I:%M %p"))
        date= str(date.strftime("%A, %B %d, %Y"))
        aboutC=aboutC+". This comment was created on "+date+" at "+time
        
        
        connection = sqlite3.connect("./cogs/DataBase/review.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM rating WHERE UserId =?", (memberId,))
        result= cursor.fetchone()

        if result is None:
            aboutC=aboutC+" this is the first review on "+member+"."
            finalMessage="You were the first person to rate"+member+"! "
            cursor.execute("INSERT INTO rating (UserId,UserName,Rates,Comments,Author,AuthorId,AboutComment) VALUES (?,?,?,?,?,?,?)",(memberId,member,rating,comment,user,userId,aboutC))
        else:
            
            allAuthorsId = result[5]
            allAuthorsId = allAuthorsId.split(" ajx ")
            length=len(allAuthorsId)
            for i in range(len(allAuthorsId)):
                if int(userId)==int(allAuthorsId[i]):
                    await interaction.response.send_message(f"You have already reviewd this person editing reviews may be added in the future",ephemeral=True)
                    connection.close
                    return
            allAuthorsId.append(userId)
            allAuthorsId = " ajx ".join(allAuthorsId)

            finalMessage=""
            allRates = result[2]
            allRates = allRates.split(" ajx ")
            allRates.append(rating)
            allRates = " ajx ".join(allRates)

            allComments = result[3]
            allComments = allComments.split(" ajx ")
            allComments.append(comment)
            allComments = " ajx ".join(allComments)

            
            allAuthors = result[4]
            allAuthors = allAuthors.split(" ajx ")
            allAuthors.append(user)
            allAuthors = " ajx ".join(allAuthors)

            aboutC=aboutC+" this is the " +str(length)+"th review on "+member+"."
            allDetail = result[6]
            allDetail = allDetail.split(" ajx ")
            allDetail.append(aboutC)
            allDetail = " ajx ".join(allDetail)
            

            cursor.execute("UPDATE rating SET Rates = ?, Comments =?, Author=?, AuthorId=? ,AboutComment=? WHERE UserId= ?" , (allRates,allComments,allAuthors,allAuthorsId,allDetail,memberId))
        connection.commit()
        connection.close()
        finalMessage="You successfully reviewed the member: "+member+". "+finalMessage+"You rated them "+rating+"/5 and your comment is "+"\""+comment+"\""+ ". Thank you for leaving a review"
        await interaction.response.send_message(finalMessage,ephemeral=True)




    @app_commands.command(name="member_lookup",description="Look up a member using either there ID or mentionin")
    async def lookup(self,interaction:discord.Interaction,new_reviews_first:bool,how_many_reviews_do_u_wanna_see:int, member_mention_or_id: discord.Member,want_extra_info:bool):
        notes=""
        
        memberId=member_mention_or_id.id

        connection = sqlite3.connect("./cogs/DataBase/review.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM rating WHERE UserId =?", (memberId,))
        result= cursor.fetchone()

        if result is None:
            await interaction.response.send_message(f"Member Not found",ephemeral=True)
        else:
            allRates = result[2]
            allRates = allRates.split(" ajx ")
            allComments = result[3]
            allComments = allComments.split(" ajx ")
            extraInfo = result[6]
            extraInfo = extraInfo.split(" ajx ")
            
            if new_reviews_first is True:
                allRates.reverse()
                allComments.reverse()
            average=0
            for rate in allRates:
                average+=int(rate)
            average/=len(allRates)
            average=round(average,2)
            notes=result[1]+"'s average rating is "+str(average)+"/5 and they have "+str(len(allRates))+" reviews."
            if how_many_reviews_do_u_wanna_see>len(allRates):
                notes=notes+" They do not have enough reviews to show "+str(how_many_reviews_do_u_wanna_see)+" reviews."
                how_many_reviews_do_u_wanna_see=len(allRates)
            for i in range(how_many_reviews_do_u_wanna_see):
                notes=notes+"\n\nComment: "+str(allComments[i])+"\nRating: "+str(allRates[i])
                if want_extra_info is True:
                    notes=notes+"\n"+extraInfo[i]
        connection.close()
        await interaction.response.send_message(notes,ephemeral=True)

async def setup(bot):
    await bot.add_cog(ReviewCommands(bot))