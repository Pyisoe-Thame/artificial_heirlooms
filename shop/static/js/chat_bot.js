// This part is the floating widget of chatbot 
(function(d, m){
var kommunicateSettings = 
{
    "appId":"ae1223135d0dc2d21398776b28ee6004","popupWidget":true,"automaticChatOpenOnNavigation":true};
    var s = document.createElement("script"); s.type = "text/javascript"; s.async = true;
    s.src = "https://widget.kommunicate.io/v2/kommunicate.app";
    var h = document.getElementsByTagName("head")[0]; h.appendChild(s);
    window.kommunicate = m; m._globals = kommunicateSettings;

    // Wait until the widget loads, then apply custom CSS
    s.onload = function() 
    {
        // Injecting custom CSS styles for the chatbot
        var style = document.createElement('style');
        style.innerHTML = `
        .km-chat-widget { 
            background-color: #8B5E3C !important;  /* Chocolate background */
        }
        .km-header, .km-chat-header { 
            background-color: #6F4E37 !important;  /* Darker header */
            color: white !important;              /* White text */
        }
        .km-msg-box { 
            background-color: #D2B48C !important; /* Lighter brown for message box */
        }
        .km-button { 
            background-color: #8B4513 !important; /* Button color */
            color: white !important;
        }
        `;
        document.head.appendChild(style);
    };
})(document, window.kommunicate || {});

