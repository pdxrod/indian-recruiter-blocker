InboxSDK.load(2, 'sdk_RecruiterFilter_0d0600ccc2').then(function(sdk){

  sdk.Conversations.registerThreadViewHandler(function(threadView){
     console.log( "Thread view:" );
     subject = threadView.getSubject();
     subject = subject.toLowerCase();
     console.log( subject );
  });

});
