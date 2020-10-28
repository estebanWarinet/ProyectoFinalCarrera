import React from 'react';
import Modal from 'react-modal';
 
const customStyles = {
  content : {
    top                   : '50%',
    left                  : '50%',
    right                 : 'auto',
    bottom                : 'auto',
    marginRight           : '-50%',
    transform             : 'translate(-50%, -50%)'
  }
};
 
// Make sure to bind modal to your appElement (http://reactcommunity.org/react-modal/accessibility/)
Modal.setAppElement('*')
 
function ModalImagenesult(props){
  var subtitle;
  const [modalIsOpen,setIsOpen] = React.useState(false);

  function afterOpenModal() {
    // references are now sync'd and can be accessed.
    subtitle.style.color = '#f00';
  }
 
  function closeModal(){
    props.onChange("openModal","openModal",false)
  }
 
    return (
      <div>
        <Modal
          isOpen={props.openModal}
          onAfterOpen={afterOpenModal}
          onRequestClose={closeModal}
          style={customStyles}
          contentLabel="Example Modal"
        >
            <h2 ref={_subtitle => (subtitle = _subtitle)}>Decaimiento de la Coherencia</h2>
            <img src={`data:image/jpeg;base64,${props.imageData}`} />
            <button className = "ui button" onClick={closeModal}>Cerrar </button>
        </Modal>
      </div>
    );
}

export default ModalImagenesult;