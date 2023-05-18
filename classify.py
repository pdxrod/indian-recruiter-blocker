#!/usr/bin/env python

import os
import random

DATA_PATH = os.path.join(os.getcwd(), "data")
SPAM = False
NOTSPAM = True
DEBUG = True

MESSAGE_VIEW_PATH = os.path.join(os.getcwd(), "messageView.js.template")
MESSAGE_NEW_PATH = os.path.join(os.getcwd(), "messageView.js")
BEGIN_ANALYZE = "/* ANALYZE FUNCTION */"

MESSAGE_VIEW = """
const phrasesArray = PHRASES;
const namesArray =   NAMES;

function analyze( messageView ) {
  let thread = messageView.getThreadView();
  let subject = thread.getSubject();
  subject = subject.toLowerCase();
  let sender = messageView.getSender();
  let name = sender[ "name" ].toLowerCase();
  let emailAddress = sender[ "emailAddress" ].toLowerCase();
  let emailArray = emailAddress.split( AT );
  let emailName = emailArray[ 0 ];
  let emailNameArray = [ emailName ];
  if( emailName.includes( DOT )) emailNameArray = emailName.split( DOT );
  emailName = emailNameArray.join( SPACE );
  let element = messageView.getBodyElement();
  let body = element.innerText;
  body = body.toLowerCase();
  bodyArray = body.split( "\\n" );
  let wholeArray = [subject, name, emailName].concat( bodyArray );
  wholeArray = removeEmpties( wholeArray );

debug( "namesArray 2: "+namesArray[ 2 ] );
debug( "phrasesArray: "+phrasesArray );
  
  p = phraseIn( phrasesArray, wholeArray, 2 );
  n = nameIn(    namesArray, wholeArray, 2   );
  console.log( emailAddress + " " + ", p is " + p + ", n is " + n );
}
"""

def debug( str ):
  if DEBUG:
    print( str )

def remove_empties_and_quotes( arr ):
  res = []
  for ele in arr:
    if ele.strip():
      res.append( ele.replace( "'", " " ))
  return res

def file2array( filename ):
  with open( filename, "r" ) as f:
    return f.read().lower().splitlines()

Names =   remove_empties_and_quotes( file2array( "names.csv" ))
Phrases = remove_empties_and_quotes( file2array( "phrases.csv" ))

# Return how many of the strings in msg contain a phrase in phr
def phrase_in( phr, msg, max ):
  count = 0
  phrases = []
  for line in msg:
    for phrase in phr:
      if count >= max: # Don't keep searching for more matches if you've reached max
        return count
      if( (phrase in line) and not (phrase in phrases) ): # Don't keep trying to match the same phrase
        debug( f"phrase {phrase}; line {line}" )
        phrases.append( phrase )
        count += 1
  return count

# Names have to be dealt with differently from phrases - a triple for loop, and == instead of in
def name_in( nms, msg, max ):
  count = 0
  names = []
  for line in msg:
    for word in line.split():
      for name in nms:
        if count >= max: # Don't keep searching for more matches if you've reached max
          return count
        if( (name == word) and not (name in names) ): # Don't keep trying to match the same name
          debug( f"name {name}; line {line}" )
          names.append( name )
          count += 1
  return count

def analyze( file ):
  email = file.read().lower()
  arr = remove_empties_and_quotes( email.splitlines() )
  max = 2
  if DEBUG:
    random.shuffle( arr )
    random.shuffle( Phrases )
    random.shuffle( Names )
    max += random.randint( 0, 1 )
  p = phrase_in( Phrases, arr, max )
  n = name_in( Names, arr, max )

# If there are two or more Indian names and one or more phrases, OR
#    there are two or more phrases and one or more Indian names, it's spam
  if( (n > 1 and p > 0) or (p > 1 and n > 0) ):
    return SPAM
  return NOTSPAM

def deal_with_file( filename, wrongly_spam, wrongly_not_spam ):
  fullname = os.path.join( DATA_PATH, filename )
  if( DEBUG ):
    print( "--- " + filename + " ---" )
  with open( fullname, 'r' ) as file:
    if SPAM == analyze( file ):
      if( filename.startswith( "not-spam") ):
        wrongly_spam.append( filename )
    else: # analyze returned NOTSPAM - it thinks it's not Indian spam
      if( filename.startswith( "spam") ):
        wrongly_not_spam.append( filename )

def write_messageview_new( arr, msg_view ):
  try:
    if os.path.exists( MESSAGE_NEW_PATH ):
      os.remove( MESSAGE_NEW_PATH )
      
    with open( MESSAGE_NEW_PATH, 'w' ) as msgnewfile:      
      for line in arr:
        if BEGIN_ANALYZE in line:
          msgnewfile.write( msg_view )
        else:
          msgnewfile.write( f'{line}\n' )
          
      msgnewfile.close()    
  except:
    print( "Problem with " + MESSAGE_NEW_PATH )

def rewrite_javascript( msg_view ):
  phrases = ','.join([ "'" + str(elem) + "'" for elem in Phrases])
   # produces a string like this '"foo","bar"'
  phrases = "[" + phrases + "]";
   # makes it into '["foo","bar"]' for putting in JavaScript, when it becomes an array
  debug("phrases: " + phrases);  

  names = ','.join([ "'" + str(elem) + "'" for elem in Names])  
  names = "[" + names + "]";
  msg_view_with_arrays = msg_view.replace( "PHRASES", phrases )
  msg_view_with_arrays = msg_view_with_arrays.replace( "NAMES", names )
  try:    
    with open( MESSAGE_VIEW_PATH, 'r' ) as msgviewfile:
      javascript = msgviewfile.read()
      arr = javascript.splitlines() 
      write_messageview_new( arr, msg_view_with_arrays )
      msgviewfile.close()
  except: 
    print( "Problem with " + MESSAGE_VIEW_PATH )

def main():
  wrongly_spam = []
  wrongly_not_spam = []
  try:
    for filename in os.listdir( DATA_PATH ):
      if( "spam" in filename ):
        deal_with_file( filename, wrongly_spam, wrongly_not_spam )
    print( "\n" )
    message_view = rewrite_javascript( MESSAGE_VIEW )
    if DEBUG:
      print( message_view )
      print( "Wrongly classified as spam: ")
      print( wrongly_spam )
      print( "Wrongly classified as not spam: ")
      print( wrongly_not_spam )

  except:
    print( "Problem with " + DATA_PATH )

# Why? See https://www.youtube.com/watch?v=g_wlZ9IhbTs
if __name__ == '__main__':
  main()
