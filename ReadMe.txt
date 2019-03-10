
Some notes:

File imap_mail(v2).py marked as version2, though there's no any version1.
That's because I wrote first version on base "imaplib" and suddenly it's appeared
that there's some object IMAP4 in it (class, a kind of mail server).
So I rewrote all on base IMAP4
I'm not sure, but it seems the application became more stable.

I plan to continue later to parse message body.
It is not so easy, because of many citings ans attachments there

In this variant, it is possible to save attachments of current message (look in menu)





