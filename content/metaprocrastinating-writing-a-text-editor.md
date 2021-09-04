Title: Metaprocrastinating on writing a book by writing a text editor
Date: 2021-09-04
Category: Programming
Description: Why I've decided to procrastinate on finishing writing my book and write a text editor instead.
Summary: If you have been following my [Essential Tools and Practices for the Aspiring Software Developer](https://blog.balthazar-rouberol.com/category/essential-tools-and-practices-for-the-aspiring-software-developer) posts and were anxious to read more, you might have noticed that they stopped coming after a while. I have a draft for the last chapter, and I regularly think about getting back to it, at least to get some closure. Alas, procrastination being what it is, I never did. My procrastination level became really interesting when I convinced myself that one of the reasons that I didn't want to write that final chapter was that my text editor was standing in the way. I was either using a full-fledged code editor (Sublime Text/VSCode) riddled with complex features I didn't need (autocompletion, linting, etc) or getting lost in configuring `vim` into the perfect markdown editor. Either way, these were the wrong tools for the job, and my only way to get back to writing was to..  write my own?
Image: https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/metaprocrastination-bo/bo.webp
Tags: Rust
Keywords: editor, rust, bo

If you have been following my [Essential Tools and Practices for the Aspiring Software Developer](https://blog.balthazar-rouberol.com/category/essential-tools-and-practices-for-the-aspiring-software-developer) posts and were anxious to read more, you might have noticed that they stopped coming after a while. I have a draft for the last chapter, and I regularly think about getting back to it, at least to get some closure. Alas, procrastination being what it is, I never did.

My procrastination level became really interesting when I convinced myself that one of the reasons that I didn't want to write that final chapter was that my text editor was standing in the way. I was either using a full-fledged code editor (Sublime Text/VSCode) riddled with complex features I didn't need (autocompletion, linting, etc) or getting lost in configuring `vim` into the perfect markdown editor. Either way, these were the wrong tools for the job, and my only way to get back to writing was to..  write my own?

And thus, [`bo`](https://github.com/brouberol/bo) was born.

<video controls>
    <source src="https://user-images.githubusercontent.com/480131/131999617-61acc5a2-4055-4cd1-9da1-134ee9e075b4.mp4" type="video/mp4">
</video>

The idea was to create a simple text editor, with powerful `vim`-like navigation. It should allow me to write in a very simple interface,
while being able to navigate through the text in a couple of keystrokes, leveraging the muscle memory I built over the years using `vim` (or the vim mode in various editors). 

I wanted it to be written in Rust, as it would be a good opportunity for me to write non-trivial code in a safe language, and also because, well, it just sounded fun.

I've been working on it on and off in the last month, and I've implemented enough features so that it's starting to feel comfortable.

![bo-help](https://balthazar-rouberol-blog.s3.eu-west-3.amazonaws.com/metaprocrastination-bo/bo-help.webp)

There's still [a lot to do](https://github.com/brouberol/bo/issues)! I'd be delighted if you wanted to test it and give it a go!

_Written with `bo`._