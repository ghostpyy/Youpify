pip install -r requirements.txt

![logo](https://github.com/ghostpyy/Youpify/blob/main/Top%20Trackify%20website/images/original.png)

## Inspiration

Top Trackify was inspired by our love of music and also the curiosity of wanting to use the Spotify API. Along the way, we ended up deciding to utilize the YouTube API on top of this to create an application that fulfills a small but useful niche.

## What it does

Top Trackify is able to get a user's top Spotify tracks and directly convert it to a YouTube playlist. In addition users are able to export their favorite playlists to YouTube as well as create a Spotify playlist with your Top Spotify Tracks.

## How we built it

We used the Spotipy Spotify API and YouTube APIs with Python to design our software application. We used HTML, CSS, and some Javascript elements to design our web page.

## Challenges we ran into

The biggest hurdle in the project has been working with the rate limit for the YouTube Data API. The max token grant rate per day is 10,000 while each API call we use takes about 50 tokens. However, tokens are not granted immediately upon signing up but are slowly generated. This was a huge issue for us since we needed to test our project immediately, and with relatively higher volumes. In the end, with a generous sleep interval between API calls, we were able to get the program to work at the last minute.

## Accomplishments that we're proud of

We were able to make a functional desktop application with all 3 features we implemented working as intended. We also made a front-end web page for our project. This was a great experience for our first hackathon.

## What we learned

We learned that communication and time management is crucial for projects that are heavily time dependent such as this one. In addition, we experienced working with multiple APIs created lots of compounding problems compared to working with a single API.

## What's next for Top Trackify

The next thing we would do with Top Trackify is to combine the UI elements with the program itself. Instead of using files with hard-coded authentication values, we want to explore other ways of using user authentication.

## Built With
css/html, javascript, python, scss
