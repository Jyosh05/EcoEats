//Function to redeem reward:
function redeemReward(rewardName) {
    try {
//    fetching user details from server
        const userResponse = await fetch('/retrieveMembershipDetails');
        const userData = await userResponse.json();
        if (!userResponse.ok) {
            throw new Error('Failed to fetch user details');
        }
        const userID = userData.id;

        const url = '/redeemReward?id = ${id} &rewardName=${rewardName}';

//        send req to server to handle redemption logic
        const response = await fetch(url, {method: 'POST'});
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        const data = await response.json();

        //handling response from server
        alert(data.message);

        //error handling
        } catch (error) {
            console.error('Error:', error);
        }
    }
}