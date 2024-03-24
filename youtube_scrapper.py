from youtube_search import YoutubeSearch
from youtube_transcript_api import YouTubeTranscriptApi

def get_eng_recipe(recipe_name, min_duration = 5):
    '''this function uses transcript api to find recipes with eng subtitles and list them,
    and returns a list of dictionaries with video details & transcript'''
    eng_recipe = []
    results = YoutubeSearch(recipe_name, max_results=100).to_dict()
    for result in results:
        # checking if the duration > min duration
        if float(result['duration'].split(':')[0]) >= min_duration: 
            try:
                transcript_list = YouTubeTranscriptApi.list_transcripts(result['id'])
                for transcript in transcript_list:
                    # check if the lang is english
                    if 'english' in transcript.language.lower():
                        result['transcript'] = YouTubeTranscriptApi.get_transcript(result['id'], ['en', 'en-GB', 'en-US'])
                        eng_recipe.append(result)
                    if len(eng_recipe) == 10:
                        break
            except:
                None
    return eng_recipe


# def get_eng_recipe(recipe_name, min_duration = 5):
#     '''this function uses transcript api to find recipes with eng subtitles and list them,
#     and returns a list of dictionaries with video details & transcript'''
#     eng_recipe = []
#     results = YoutubeSearch(recipe_name, max_results=100).to_dict()
#     for result in results:
#         # checking if the duration > min duration
#         if float(result['duration'].split(':')[0]) >= min_duration: 
#             try:
#                 transcript_list = YouTubeTranscriptApi.list_transcripts(result['id'])
#                 for transcript in transcript_list:
#                     # check if the lang is english
#                     if 'english' in transcript.language.lower():
#                         # result['transcript'] = YouTubeTranscriptApi.get_transcript(result['id'], ['en', 'en-GB', 'en-US'])
#                         eng_recipe.append(result)
#                     if len(eng_recipe) == 10:
#                         break
#             except:
#                 pass
#     return eng_recipe

def get_transcript(video_id):
    return YouTubeTranscriptApi.get_transcript(video_id, ['en', 'en-GB', 'en-US'])