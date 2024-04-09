#ifndef DELETEROOMFORM_H
#define DELETEROOMFORM_H

#include <QWidget>

#include "baseform.h"

namespace Ui {
class DeleteRoomForm;
}

class DeleteRoomForm : public QWidget, public BaseForm
{
    Q_OBJECT

public:
    explicit DeleteRoomForm(QWidget *parent = nullptr);
    ~DeleteRoomForm();

    void clear() override;

private slots:
    void on_deleteRoomBtn_clicked();

signals:
    void sendData(const QString &data);

private:
    Ui::DeleteRoomForm *ui;
};

#endif // DELETEROOMFORM_H
