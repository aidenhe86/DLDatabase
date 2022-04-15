mainDeck = [];
extraDeck = [];

// read saved main deck
for(let card of $("#mainDeck").children()){
    mainDeck.push(card.alt)
}

// read saved extra deck
for(let card of $("#extraDeck").children()){
    extraDeck.push(card.alt)
}

// Add card to deck
$(".cardlist").on("click",function(e){
    e.preventDefault();

    // select card li
    const $target = $(e.target).closest("li");
    // get card id from li
    const cardID = $target.attr("id");
    // get card type
    const cardType = $target.find("h5").attr("class");

    cardImg = `<img src="https://storage.googleapis.com/ygoprodeck.com/pics_small/${cardID}.jpg" alt="${cardID}"></img>`;

    // add to deck
    if(extraMonsterType.includes(cardType)){
        // check if reach card limit in extra deck
        if(!(cardLimit(extraDeck,cardID,7))){
            $("#extraDeck").append(cardImg);
            extraDeck.push(cardID);
        }
        else{
            alert("Reach Limit!");
        }
    }
    else if(cardType !== undefined){
        // check if reach card limit in main deck
        if(!(cardLimit(mainDeck,cardID,30))){
            $("#mainDeck").append(cardImg);
            mainDeck.push(cardID);
        }
        else{
            alert("Reach Limit!");
        }
    }

})

// check card limit, if reach return true, else return false
function cardLimit(arr,cardID,maximum){
    let c = arr.filter(function(v){
        return v === cardID;
    })

    // single card limit 3, main deck limit 30, extra deck limit 7
    if((c.length < 3) && (arr.length < maximum)){
        return false;
    }
    else{
        return true;
    }
}

// remove added card
$(".deck").on("click",function(e){
    e.preventDefault();

    const $target = $(e.target).closest("img");
    const cardID = $target.attr("alt");

    if(mainDeck.includes(cardID)){
        let idx = mainDeck.indexOf(cardID);
        mainDeck.splice(idx,1);
        $target.remove();
    }
    else if (extraDeck.includes(cardID)){
        let idx = extraDeck.indexOf(cardID);
        extraDeck.splice(idx,1);
        $target.remove();
    }
})

// submit deck to python API
$("#deckForm").on("submit",async function(e){
    e.preventDefault();

    if(mainDeck.length < 20){
        alert("Main Deck must have at least 20 cards!")
        return;
    }

    const deck = {};
    const name = $("#formName").val();
    deck["name"] = name;

    // insert main deck
    for(let i=1; i <= mainDeck.length; i++){
        deck[`md${i}_id`] = mainDeck[i-1];
    }

    // insert side deck
    for(let i=1; i <= extraDeck.length;i++){
        deck[`ed${i}_id`] = extraDeck[i-1];
    }

    // check if add deck or edit deck
    let $mode = $("#deckForm").data("mode");

    // if add deck
    if($mode === "add"){
        await axios.post(`/decks/add`,deck);
    }
    // if edit deck
    else{
        await axios.post(`/decks/${$mode}/edit`,deck)
    }

    window.location.href = "/decks";
})