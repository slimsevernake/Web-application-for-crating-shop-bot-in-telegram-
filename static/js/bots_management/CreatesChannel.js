class ChannelsList {
    constructor(data) {
        this.data = data;
        this.channelsList = null;
        this.container = null;
    }

    listInit() {
        this.container = this.makeContainer();
        let items = this.makeItems(this.data);
        this.container.insertAdjacentHTML("afterBegin", items);
        this.channelsList = this.container;
        
        return this;
    }

    makeContainer() {
        if(!!document.querySelector('.main__channel-container')) {
            document.querySelector('.main__channel-container').remove();
        }

        let wrapper = document.createElement('div');
        wrapper.classList.add('main__channel-container');
            
        return wrapper;
    }

    makeItems(items) {
        let itemsList = '';
        
        for(let i = 0; i < items.length; i++) {
            let item = `<div id=${items[i].id} class="main__channel-block">
                            <span>${items[i].name} <span class="fa fa-arrow-down"></span></span>
                            <label for="modal-controller" class="main__edit fa fa-lg fa-pencil" aria-hidden="true"></label>                               
                        </div>`;
            itemsList += item;
        }

        /* <span class="main__remove fa fa-lg fa-trash"></span>   */
        
        return itemsList;
    }

    getChannel(id) {
        let item = null;

        for(let i = 0; i < this.data.length; i++) {
            if(this.data[i].id == id) {
                item = this.data[i];
            }
        }

        return item;
    }

    addItem() {
        this.data.push({id: this.data.length+1, name: 'Новий канал'});

        this.listInit();
    }

    removeItem(elem) {
        this.data = this.data.filter(function(item) { 
            return item.id != elem.id;
        })
            
        console.log(this.data);
        this.listInit();
        // this.data.forEach((item, index) => item.id = index + 1);        
    }

    render(selector) {
        document.querySelector(selector).append(this.channelsList);
    }
}