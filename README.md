# Secret-Santa-Discord-Bot
### Rendition of Speebot - festive edition (to serve single purpose of making secret santa work)

So, you wanna run a Secret Santa? No problem! I speedran this code to bring something usable to production.

The commands are down below.

## Commands:
### `/register` `name` `user (opt)` `interests (opt)` `dislikes (opt)`
- **Registers a user for Secret Santa.** If no user is given, it uses the command sender instead.
- Interests and dislikes are optional, but ***highly encouraged***.

## `/assign`
- **Assigns all participants someone to send a gift to, and someone to receive a gift from.**
- Note: **This operation is irreversible.** *(Not in theory, but in practice. I'm too lazy to implement it.)*

## `/assigned`
- **Allows the user to see who they were assigned to gift for.**
- Note: if the Secret Santas haven't been assigned, it will send a message to let you know.

## `/nudge` `message (opt)`
- **Allows the gifter to tell their recipient to give some more details.** Optionally, send a message to them anonymously as well.
- Note: if the Secret Santas haven't been assigned, it will send a message to let you know.

## `/participants`
- **Shows all participants in Secret Santa.**
- Yes, it mentions them, but it sends a silent message so no notifications will be sent.