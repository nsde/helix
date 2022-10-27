// EmojiKeyboard
let inputField = document.getElementById('message-input');

let emojiKeyboard = new EmojiKeyboard;

emojiKeyboard.callback = (emoji, closed) => {
    inputField.value = inputField.value + emoji.emoji;
    inputField.focus();
};

emojiKeyboard.resizable = true;
emojiKeyboard.default_placeholder = 'Search Emojis...';
emojiKeyboard.instantiate(document.getElementById('emoji-picker'))

// PopUps
var isRoomChooserOpen = false;

let roomDetails = document.getElementById('room-details-popup').style
let menuChooser = document.getElementById('room-chooser').style
let chatBox = document.getElementById('chat-box').style
let userProfile = document.getElementById('user-profile').style
let profilePopup = document.getElementById('profile-popup').style
let deletionWarning = document.getElementById('deletion-warning').style
let newPopup = document.getElementById('new-popup').style

function hideChat() {
    chatBox.display = 'none';
    userProfile.display = 'none';
}

function showChat() {
    userProfile.display = 'inherit';
    chatBox.display = 'inherit';
}

function accountDeletionWarning() {
    deletionWarning.height = '100%';
    deletionWarning.opacity = '1';
}

// Profile Window
function openProfileOnMobile() {
    profilePopup.height = '100%';
    profilePopup.opacity = '1';
}

function openProfile() {
    hideChat();
    openProfileOnMobile();
}

function closeProfile() {
    if (window.innerWidth > 1200) {
        showChat();
    }
    profilePopup.height = '0%';
    profilePopup.opacity = '0';
}

// New Rooms Popup
function openNew() {
    hideChat();
    newPopup.height = '100%';
    newPopup.opacity = '1';
}

function closeNew() {
    newPopup.height = '0%';
    newPopup.opacity = '0';
    closeProfile();
}

// Room Details Popup
function openRoomDetails() {
    if (!isRoomChooserOpen) {
        roomDetails.height = '100%';
        roomDetails.opacity = '1';
    }
}

function closeRoomDetails() {
    roomDetails.height = '0%';
    roomDetails.opacity = '0';
}

// Room Chooser On Mobile
function openRoomChooser() {
    isRoomChooserOpen = true;
    
    if (window.innerWidth < 1200) {
        hideChat();
    }
    
    menuChooser.display = 'inherit';
    menuChooser.width = '100%';
    menuChooser.opacity = '1';
}

function closeRoomChooser() {
    isRoomChooserOpen = false;

    chatBox.display = 'none';
    if (window.innerWidth > 1200) {
        showChat();
    }
    chatBox.display = 'none';

    menuChooser.width = '0%';
    menuChooser.opacity = '0';
}

// Key Bindings
document.onkeydown = function(e) {
    if (e.code == 'Escape') {
        if (isRoomChooserOpen) {
            closeRoomChooser();
        }

        closeProfile();
        closeNew();
        closeRoomDetails();
        inputField.focus();
    }
}

document.getElementById('emoji-picker').onclick = function(e) {
    try {
        if (!(kb.classList.contains('emojikb-hidden'))) {
            emojiKeyboard.toggle_window();
        }
    } catch {}
};
